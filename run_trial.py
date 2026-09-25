#!/usr/bin/env python
"""CogAlpha trial runner.

  .venv/bin/python run_trial.py --config config/smoke.yaml        # ~5 LLM calls, end-to-end check
  .venv/bin/python run_trial.py --config config/trial.yaml        # scaled-down paper setup
  .venv/bin/python run_trial.py --config config/trial.yaml --resume runs/<dir>   # after a usage limit
  .venv/bin/python run_trial.py --report-only runs/<dir>          # re-run the out-of-sample report
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/trial.yaml")
    ap.add_argument("--resume", type=Path, help="existing run directory to continue")
    ap.add_argument("--report-only", type=Path, help="existing run directory: only build the final report")
    ap.add_argument("--data-only", action="store_true", help="download/cache data and exit")
    args = ap.parse_args()

    run_dir = args.resume or args.report_only
    if run_dir:
        cfg = yaml.safe_load((run_dir / "config.yaml").read_text())
    else:
        cfg = yaml.safe_load((ROOT / args.config).read_text())

    if args.data_only:
        from cogalpha import data
        panel = data.load_panel(cfg["data"])
        print(f"{panel.index.get_level_values('ticker').nunique()} tickers, "
              f"{panel.index.get_level_values('date').nunique()} days, {len(panel)} rows")
        return

    if not run_dir:
        run_dir = ROOT / "runs" / f"{time.strftime('%Y%m%d_%H%M%S')}_{cfg['run_name']}"
        run_dir.mkdir(parents=True)
        (run_dir / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))

    from cogalpha.evolve import Trial
    from cogalpha.final import report

    logf = (run_dir / "run.log").open("a")

    def log(msg):
        line = f"{time.strftime('%H:%M:%S')} {msg}"
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    trial = Trial(cfg, run_dir, log)
    finished = True if args.report_only else trial.run()
    if not finished:
        return
    log("Building out-of-sample report ...")
    res = report(trial, run_dir / "report.json")
    for name, s in res["sets"].items():
        c = s["combined_test"]
        log(f"{name:17s} n={s['n_factors']:3d}  test IC={c['ic']:.4f} RankIC={c['rank_ic']:.4f} "
            f"ICIR={c['icir']:.3f} RankICIR={c['rank_icir']:.3f} AER={c['AER']:.3f} IR={c['IR']:.2f}")
    log(f"Report: {run_dir / 'report.json'}  Factors: {run_dir / 'elite_factors.py'}")


if __name__ == "__main__":
    main()
