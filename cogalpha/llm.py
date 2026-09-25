"""LLM backend: headless Claude Code (`claude -p`) billed to the logged-in claude.ai subscription.

Every call is single-turn, tool-less, and runs from an empty cwd with no settings/MCP/CLAUDE.md,
so the model sees only the CogAlpha system message and the assembled prompt.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import threading
import time
from pathlib import Path


class QuotaExhausted(RuntimeError):
    """Usage limit hit (subscription window or this run's max_calls). Checkpoint and stop."""


class ClaudeCLI:
    def __init__(self, system: str, log_path: Path, timeout_s: int = 300, max_calls: int = 150):
        self.system = system
        self.log_path = log_path
        self.timeout_s = timeout_s
        self.max_calls = max_calls
        self.calls = 0
        self.cost_usd = 0.0  # notional API-equivalent cost reported by the CLI; Pro is flat-rate
        self._lock = threading.Lock()
        self._cwd = tempfile.mkdtemp(prefix="cogalpha_llm_")

    def __call__(self, prompt: str, model: str, role: str, thinking_tokens: int | None = None) -> str:
        with self._lock:
            if self.calls >= self.max_calls:
                raise QuotaExhausted(f"max_calls={self.max_calls} reached")
            self.calls += 1
        cmd = ["claude", "-p", "--model", model, "--system-prompt", self.system, "--tools", "",
               "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config",
               "--disable-slash-commands", "--output-format", "json"]
        env = dict(os.environ)
        if thinking_tokens is not None:  # caps extended thinking, which otherwise dominates quota use
            env["MAX_THINKING_TOKENS"] = str(thinking_tokens)
        for attempt in range(3):
            t0 = time.time()
            try:
                proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                                      timeout=self.timeout_s, cwd=self._cwd, env=env)
                out = json.loads(proc.stdout)
            except subprocess.TimeoutExpired:
                out = {"is_error": True, "result": "timeout"}
            except json.JSONDecodeError:
                out = {"is_error": True, "result": (proc.stderr or proc.stdout)[-500:]}
            text = out.get("result") or ""
            self._log(role, model, prompt, out, time.time() - t0)
            if not out.get("is_error"):
                with self._lock:
                    self.cost_usd += out.get("total_cost_usd") or 0.0
                return text
            if "limit" in text.lower() and ("usage" in text.lower() or "reset" in text.lower()):
                raise QuotaExhausted(text)
            time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"claude -p failed for {role}: {text[:300]}")

    def _log(self, role, model, prompt, out, secs):
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "role": role, "model": model, "secs": round(secs, 1),
               "is_error": out.get("is_error"), "usage": out.get("usage"), "prompt": prompt,
               "response": out.get("result")}
        with self._lock, self.log_path.open("a") as f:
            f.write(json.dumps(rec) + "\n")
