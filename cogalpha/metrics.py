"""Fitness metrics (paper Sec. 3.4 / App. B.3) and qualified/elite selection."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

METRICS = ["ic", "rank_ic", "icir", "rank_icir", "mi"]


def _rowwise_corr(x: pd.DataFrame, y: pd.DataFrame) -> pd.Series:
    mask = x.notna() & y.notna()
    x, y = x.where(mask), y.where(mask)
    xd, yd = x.sub(x.mean(axis=1), axis=0), y.sub(y.mean(axis=1), axis=0)
    num = (xd * yd).sum(axis=1)
    den = np.sqrt((xd ** 2).sum(axis=1) * (yd ** 2).sum(axis=1))
    corr = num / den.replace(0, np.nan)
    return corr[mask.sum(axis=1) >= 10]


def daily_ic(factor: pd.Series, label: pd.Series, rank: bool = False) -> pd.Series:
    f = factor.replace([np.inf, -np.inf], np.nan).unstack("ticker")
    r = label.reindex(factor.index).unstack("ticker")
    if rank:
        f, r = f.rank(axis=1), r.rank(axis=1)
    return _rowwise_corr(f, r)


def evaluate(factor: pd.Series, label: pd.Series, mi_samples: int = 50000, seed: int = 0) -> dict:
    ic, ric = daily_ic(factor, label), daily_ic(factor, label, rank=True)
    # MI on per-day cross-sectional ranks (scale-free, comparable across factors)
    f = factor.replace([np.inf, -np.inf], np.nan).groupby(level="date").rank(pct=True)
    r = label.reindex(factor.index).groupby(level="date").rank(pct=True)
    xy = pd.concat([f, r], axis=1).dropna().to_numpy()
    if len(xy) > mi_samples:
        xy = xy[np.random.default_rng(seed).choice(len(xy), mi_samples, replace=False)]
    mi = float(mutual_info_regression(xy[:, :1], xy[:, 1], random_state=seed)[0]) if len(xy) > 100 else 0.0
    return {
        "ic": float(ic.mean()), "rank_ic": float(ric.mean()),
        "icir": float(ic.mean() / ic.std()) if ic.std() > 0 else 0.0,
        "rank_icir": float(ric.mean() / ric.std()) if ric.std() > 0 else 0.0,
        "mi": mi, "n_days": int(len(ic)),
    }


def score(m: dict) -> float:
    """Sign-agnostic composite used for ranking (a model can flip a negatively-predictive factor)."""
    return abs(m["rank_ic"]) + abs(m["ic"]) + 0.1 * (abs(m["icir"]) + abs(m["rank_icir"])) + m["mi"]


def select(metric_rows: dict[str, dict], cfg: dict) -> tuple[list[str], list[str]]:
    """(qualified, elite) names: every metric must beat both the generation percentile and a floor.
    IC-type metrics are compared in absolute value."""
    if not metric_rows:
        return [], []
    df = pd.DataFrame(metric_rows).T[METRICS].astype(float)
    df[["ic", "rank_ic", "icir", "rank_icir"]] = df[["ic", "rank_ic", "icir", "rank_icir"]].abs()

    def passing(pct, floors):
        thr = np.maximum(df.quantile(pct / 100.0), pd.Series(floors)[METRICS])
        return df.index[(df >= thr).all(axis=1)].tolist()

    return passing(cfg["qualified_pct"], cfg["qualified_min"]), passing(cfg["elite_pct"], cfg["elite_min"])
