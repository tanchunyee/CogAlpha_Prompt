"""Parse LLM factor code, run it in a restricted child process, and apply the paper's
execution / numerical-stability / temporal-leakage checks (Appendix A.3)."""
from __future__ import annotations

import ast
import builtins
import math
import multiprocessing as mp
import re
import traceback
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

_FUNC_BLOCK = re.compile(r"<<function\s*\d*>>(.*?)<</function\s*\d*>>", re.S)
_ALLOWED_IMPORTS = {"numpy", "pandas", "scipy", "talib", "math"}
_BANNED_NAMES = {"open", "exec", "eval", "compile", "globals", "locals", "vars", "input",
                 "breakpoint", "exit", "quit", "__import__", "setattr", "delattr"}


@dataclass
class Factor:
    name: str
    code: str
    agent: str
    origin: str                       # initial | mutation | crossover | crossover_mutation | inject
    generation: int = 0
    parents: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    status: str = "new"               # new | failed | evaluated
    fail_reason: str = ""
    history: list[str] = field(default_factory=list)


def parse_functions(text: str) -> list[tuple[str, str]]:
    """[(name, code)] for every <<function N>> block (falls back to bare `def` blocks)."""
    blocks = _FUNC_BLOCK.findall(text) or ([text] if "def factor_" in text else [])
    out = []
    for block in blocks:
        code = re.sub(r"^\s*```(?:python)?\s*$", "", block, flags=re.M).strip("\n")
        code = _dedent(code)
        try:
            tree = ast.parse(code)
        except SyntaxError:
            m = re.search(r"def\s+(\w+)\s*\(", code)
            if m:
                out.append((m.group(1), code))
            continue
        fns = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if fns:
            out.append((fns[-1].name, code))
    return out


def _dedent(code: str) -> str:
    lines = code.splitlines()
    start = next((i for i, l in enumerate(lines) if l.lstrip().startswith("def ")), 0)
    indent = len(lines[start]) - len(lines[start].lstrip()) if lines else 0
    return "\n".join(l[indent:] if l[:indent].strip() == "" else l for l in lines[start:])


def static_check(code: str) -> str | None:
    """Return an error string, or None if the code passes the static rules."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"SyntaxError: {e}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            bad = [m for m in mods if m.split(".")[0] not in _ALLOWED_IMPORTS]
            if bad:
                return f"Forbidden import: {bad}"
        if isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            return f"Forbidden name: {node.id}"
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return f"Forbidden dunder attribute: {node.attr}"
        if isinstance(node, (ast.For, ast.While)):
            if isinstance(node, ast.While) and isinstance(node.test, ast.Constant) and node.test.value:
                return "Forbidden: `while True` / potentially infinite loop"
            for inner in ast.walk(node):
                if inner is not node and isinstance(inner, (ast.For, ast.While)):
                    return "Forbidden: nested loops"
    return None


def _safe_import(name, *args, **kwargs):
    if name.split(".")[0] not in _ALLOWED_IMPORTS:
        raise ImportError(f"import of {name!r} is not allowed")
    return __import__(name, *args, **kwargs)


def _namespace() -> dict:
    import talib
    from scipy import stats
    safe_builtins = {k: getattr(builtins, k) for k in dir(builtins) if k not in _BANNED_NAMES}
    safe_builtins["__import__"] = _safe_import
    return {"__builtins__": safe_builtins, "np": np, "pd": pd, "stats": stats, "talib": talib, "math": math}


def _apply(func, panel: pd.DataFrame, name: str) -> pd.Series:
    parts = []
    for _, g in panel.groupby(level="ticker", sort=False):
        out = func(g.copy())
        if isinstance(out, pd.DataFrame) and out.shape[1] == 1:
            out = out.iloc[:, 0]
        if not isinstance(out, pd.Series):
            if np.ndim(out) == 1 and len(out) == len(g):
                out = pd.Series(np.asarray(out, dtype=float), index=g.index)
            else:
                raise TypeError(f"factor must return a pd.Series, got {type(out).__name__}")
        if len(out) != len(g) or not out.index.equals(g.index):
            out = out.reindex(g.index)
        parts.append(pd.to_numeric(out, errors="coerce").astype(float))
    return pd.concat(parts).rename(name)


def _worker(code, name, panel, cutoff, q):
    try:
        ns = _namespace()
        exec(compile(code, f"<{name}>", "exec"), ns)
        func = ns[name]
        with np.errstate(all="ignore"):
            full = _apply(func, panel, name)
            trunc = _apply(func, panel[panel.index.get_level_values("date") <= cutoff], name)
        q.put(("ok", full, trunc))
    except Exception:
        q.put(("error", traceback.format_exc(limit=4)[-1500:], None))


_CTX = None


def _mp_context():
    """forkserver (not fork): the caller runs LLM calls in threads, and forking a threaded process is unsafe."""
    global _CTX
    if _CTX is None:
        _CTX = mp.get_context("forkserver")
        _CTX.set_forkserver_preload(["numpy", "pandas", "scipy.stats", "talib", "cogalpha.factors"])
    return _CTX


def execute(code: str, name: str, panel: pd.DataFrame, timeout_s: int = 60):
    """Run the factor on the full panel and on a truncated panel (for the leakage test).
    Returns (full_series, truncated_series, error)."""
    dates = panel.index.get_level_values("date").unique().sort_values()
    cutoff = dates[int(len(dates) * 0.6)]
    ctx = _mp_context()
    q = ctx.Queue()
    p = ctx.Process(target=_worker, args=(code, name, panel, cutoff, q), daemon=True)
    p.start()
    try:
        status, a, b = q.get(timeout=timeout_s)
    except Exception:
        p.kill()
        return None, None, f"Execution timed out after {timeout_s}s (too slow / possible infinite loop)"
    finally:
        p.join(timeout=5)
    return (a, b, None) if status == "ok" else (None, None, a)


def numeric_check(values: pd.Series, train_mask: np.ndarray, max_nan: float, min_distinct: int) -> str | None:
    v = values.replace([np.inf, -np.inf], np.nan)
    n_inf = int(np.isinf(values.to_numpy()).sum())
    nan_ratio = float(v[train_mask].isna().mean())
    if nan_ratio > max_nan:
        return f"NaN ratio {nan_ratio:.1%} exceeds {max_nan:.0%}" + (f" ({n_inf} inf values)" if n_inf else "")
    distinct = v[train_mask].groupby(level="date").nunique()
    if distinct.median() < min_distinct:
        return f"Degenerate factor: median {distinct.median():.0f} distinct values per day"
    return None


def leakage_check(full: pd.Series, trunc: pd.Series) -> str | None:
    """Values up to the cutoff must not change when future rows are removed."""
    a = full.reindex(trunc.index).to_numpy()
    b = trunc.to_numpy()
    both_nan = np.isnan(a) & np.isnan(b)
    close = np.isclose(a, b, rtol=1e-6, atol=1e-9) | both_nan
    bad = int((~close).sum())
    if bad:  # a causal factor reproduces its history exactly, so any change is leakage
        return (f"Temporal leakage: {bad} historical values changed when future data was removed "
                "(e.g. shift(-k), centered windows, full-sample normalisation, bfill)")
    return None
