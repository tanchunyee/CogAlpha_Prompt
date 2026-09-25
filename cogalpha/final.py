"""Out-of-sample evaluation of the final candidate pool (paper Sec. 4.1 'Evaluation', simplified).

The paper trains LightGBM/Ridge on the mined alphas with Qlib and backtests top-50/drop-5.
Here: one model trained on the train split (valid for early stopping), scored on test, plus a
daily top-k long portfolio vs the equal-weight universe. A classic-factor baseline gets the same
treatment so the trial has a reference point.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import factors as F
from . import metrics as M

BASELINE = {
    "mom_20": "def mom_20(df):\n    return df['close'].pct_change(20)",
    "rev_5": "def rev_5(df):\n    return -df['close'].pct_change(5)",
    "vol_20": "def vol_20(df):\n    return df['close'].pct_change().rolling(20).std()",
    "volu_ratio_5_20": "def volu_ratio_5_20(df):\n    return df['volume'].rolling(5).mean() / df['volume'].rolling(20).mean()",
    "range_20": "def range_20(df):\n    return ((df['high'] - df['low']) / df['close']).rolling(20).mean()",
    "close_pos_20": "def close_pos_20(df):\n    lo, hi = df['low'].rolling(20).min(), df['high'].rolling(20).max()\n"
                    "    return (df['close'] - lo) / (hi - lo + 1e-12)",
}


def _split(idx: pd.MultiIndex, span) -> np.ndarray:
    d = idx.get_level_values("date")
    return np.asarray((d >= span[0]) & (d <= span[1]))


def compute(codes: dict[str, str], panel: pd.DataFrame, timeout_s: int) -> pd.DataFrame:
    cols = {}
    for name, code in codes.items():
        full, _, err = F.execute(code, name, panel, timeout_s)
        if err is None:
            cols[name] = full.reindex(panel.index).replace([np.inf, -np.inf], np.nan)
    return pd.DataFrame(cols, index=panel.index)


def _cs_rank(x: pd.DataFrame | pd.Series):
    return x.groupby(level="date").rank(pct=True)


def combine(X: pd.DataFrame, label: pd.Series, cfg: dict, fcfg: dict) -> pd.Series:
    Xr = _cs_rank(X).fillna(0.5)
    y = _cs_rank(label)
    tr, va = _split(X.index, cfg["train"]), _split(X.index, cfg["valid"])
    ok = y.notna().to_numpy()
    if fcfg["model"] == "ridge":
        from sklearn.linear_model import Ridge
        model = Ridge(alpha=10).fit(Xr[tr & ok], y[tr & ok])
    else:
        import lightgbm as lgb
        model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.02, num_leaves=32, max_depth=8,
                                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                                  reg_alpha=1.0, reg_lambda=1.0, verbose=-1)
        model.fit(Xr[tr & ok], y[tr & ok], eval_X=Xr[va & ok], eval_y=y[va & ok],
                  callbacks=[lgb.early_stopping(50, verbose=False)])
    return pd.Series(model.predict(Xr), index=X.index, name="pred")


def portfolio(pred: pd.Series, panel: pd.DataFrame, span, top_k: int, n_drop: int, cost_bps: float) -> dict:
    """Qlib-style TopK-Dropout: hold top_k names equally weighted, swap at most n_drop per day
    (worst held out, best unheld in); trade at next open; excess vs equal-weight universe."""
    op = panel["open"].groupby(level="ticker")
    ret1 = (op.shift(-2) / op.shift(-1) - 1).unstack("ticker")
    p = pred[_split(pred.index, span)].unstack("ticker")
    ret1 = ret1.reindex(p.index)
    held, rows = [], []
    for _, s in p.iterrows():
        s = s.dropna()
        held = [t for t in held if t in s.index]
        best_new = s.drop(held).nlargest(max(top_k - len(held), n_drop)).index.tolist()
        drop = s[held].nsmallest(n_drop).index.tolist() if len(held) >= top_k else []
        keep = [t for t in held if t not in drop]
        held = keep + best_new[:top_k - len(keep)]
        rows.append(pd.Series(1.0 / len(held), index=held) if held else pd.Series(dtype=float))
    w = pd.DataFrame(rows, index=p.index).reindex(columns=p.columns).fillna(0.0)
    turnover = w.diff().abs().sum(axis=1).fillna(w.sum(axis=1))
    excess = (w * ret1.fillna(0)).sum(axis=1) - ret1.mean(axis=1) - turnover * cost_bps / 1e4
    excess = excess.dropna()
    return {"AER": float(excess.mean() * 252),
            "IR": float(excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0.0,
            "avg_daily_turnover": float(turnover.mean())}


def report(trial, out: Path) -> dict:
    cfg, fcfg = trial.cfg["data"], trial.cfg["final"]
    factors = {f["name"]: f for a in trial.state["agents"].values() for f in a["factors"]}
    elite = sorted({n for a in trial.state["agents"].values() for n in a["elite"]})
    if not elite:  # nothing crossed the elite bar: fall back to the best evaluated factors
        ev = [f for f in factors.values() if f["status"] == "evaluated"]
        elite = [f["name"] for f in sorted(ev, key=lambda f: M.score(f["metrics"]), reverse=True)[:20]]
    to = trial.cfg["quality"]["exec_timeout_s"]
    panel, label = trial.panel, trial.label

    results = {"n_candidates": len(elite), "sets": {}}
    for set_name, codes in [("cogalpha", {n: factors[n]["code"] for n in elite}), ("baseline_classic", BASELINE)]:
        X = compute(codes, panel, to)
        if X.empty:
            continue
        per_factor = {}
        for split in ("valid", "test"):
            m = _split(X.index, cfg[split])
            per_factor[split] = {c: M.evaluate(X[c][m], label, trial.cfg["fitness"]["mi_samples"]) for c in X}
        pred = combine(X, label, cfg, fcfg)
        test = _split(pred.index, cfg["test"])
        results["sets"][set_name] = {
            "n_factors": X.shape[1],
            "combined_test": {**M.evaluate(pred[test], label), **portfolio(pred, panel, cfg["test"], fcfg["top_k"], fcfg.get("n_drop", 2), fcfg["cost_bps"])},
            "per_factor": per_factor,
        }
    out.write_text(json.dumps(results, indent=1))
    (out.parent / "elite_factors.py").write_text(
        "# Final candidate pool from this CogAlpha run.\n# Pre-imported: np, pd, stats (scipy), talib, math\n\n"
        + "\n\n\n".join(f"# agent={factors[n]['agent']} origin={factors[n]['origin']} gen={factors[n]['generation']} "
                        f"train={json.dumps({k: round(v, 4) for k, v in factors[n]['metrics'].items()})}\n{factors[n]['code']}"
                        for n in elite) + "\n")
    return results
