"""OHLCV panel download/caching and forward-return labels."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from .universes import UNIVERSES

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FIELDS = ["open", "high", "low", "close", "volume"]

COLUMN_DESCRIPTIONS = {
    "open": "Daily opening price (split/dividend adjusted).",
    "high": "Daily highest traded price (adjusted).",
    "low": "Daily lowest traded price (adjusted).",
    "close": "Daily closing price (adjusted).",
    "volume": "Daily traded volume in shares.",
}


def tickers_for(universe) -> list[str]:
    return list(universe) if isinstance(universe, list) else UNIVERSES[universe]


def load_panel(cfg: dict, refresh: bool = False) -> pd.DataFrame:
    """Return a (date, ticker)-indexed OHLCV frame, sorted by ticker then date."""
    tickers = tickers_for(cfg["universe"])
    key = hashlib.md5(json.dumps([tickers, cfg["start"], cfg["end"]]).encode()).hexdigest()[:10]
    path = DATA_DIR / f"ohlcv_{cfg['source']}_{key}.pkl"
    if path.exists() and not refresh:
        return pd.read_pickle(path)
    if cfg["source"] != "yfinance":
        raise ValueError(f"unsupported data source {cfg['source']!r}")

    import yfinance as yf

    raw = yf.download(tickers, start=cfg["start"], end=cfg["end"], auto_adjust=True,
                      group_by="column", progress=False, threads=True)
    panel = (raw[[f.capitalize() for f in FIELDS]]
             .stack(level=1, future_stack=True)
             .rename(columns=str.lower)
             .rename_axis(["date", "ticker"]))
    panel = panel.dropna(subset=["close"]).astype(float)
    panel = panel[panel["volume"] > 0]
    panel = panel.swaplevel().sort_index().swaplevel()  # rows grouped by ticker, chronological
    DATA_DIR.mkdir(exist_ok=True)
    panel.to_pickle(path)
    return panel


def forward_return(panel: pd.DataFrame, horizon: int) -> pd.Series:
    """Buy at next open, sell at the open `horizon` days later (Qlib-style label)."""
    op = panel["open"].groupby(level="ticker")
    return (op.shift(-(horizon + 1)) / op.shift(-1) - 1).rename("label")


def columns_desc(panel: pd.DataFrame) -> str:
    return "\n".join(f"- `{c}`: {COLUMN_DESCRIPTIONS.get(c, '')}" for c in panel.columns)
