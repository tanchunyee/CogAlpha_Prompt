# CogAlpha trial workspace

Goal: trial the idea of *Cognitive Alpha Mining via LLM-Driven Code-Based Evolution* (ACL 2026,
PDF in repo root, arXiv 2511.18850) using the owner's **Claude Pro subscription** as the LLM.

## What is upstream vs. local
- Upstream repo (`README.md`, `prompts/`, `assets/`) = the paper's prompt templates **only**. No runtime
  code, data, or evaluator was released. Do not edit `prompts/`; treat it as the paper's artifact.
- Everything else was added locally to make it runnable: `cogalpha/` (harness), `run_trial.py`,
  `config/*.yaml`, `requirements.txt`, `.venv/`, `data/` (cached OHLCV), `runs/` (outputs).

## Setup (already done 2026-09-25)
- `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (system Python 3.14; TA-Lib ≥0.6
  wheels bundle the C lib). pandas pinned `<3` because the prompts promise pandas 2.x semantics.
- LLM backend = `claude -p` (headless Claude Code, logged in via claude.ai → billed to Pro, no API key).
  Calls are single-turn, `--tools ""`, empty cwd, no settings/MCP, `MAX_THINKING_TOKENS` capped per role.
- Data = yfinance daily OHLCV for ~100 S&P 100 names 2014–2025, cached in `data/`
  (`run_trial.py --data-only` to (re)download). Current constituents ⇒ survivorship bias.

## Running
```
.venv/bin/python run_trial.py --config config/smoke.yaml           # ~13 calls, ~3 min
.venv/bin/python run_trial.py --config config/trial.yaml           # 3 agents × 3 gens, ~200–300 calls
.venv/bin/python run_trial.py --resume runs/<dir>                  # continue after a usage limit
.venv/bin/python run_trial.py --report-only runs/<dir>             # rebuild out-of-sample report
```
Outputs per run: `run.log`, `llm_calls.jsonl` (every prompt/response/usage), `state.json`
(all factors + metrics, checkpointed each generation), `report.json`, `elite_factors.py`.
When Pro's usage window runs out (or `llm.max_calls` is hit) the run checkpoints and exits; resume later.

## Pipeline (cogalpha/evolve.py) vs. paper
1. Seven-level agent generates `num_per_request` factors (guidance optionally paraphrased: light/moderate/
   creative/divergent/concrete).
2. Quality checker: static AST rules (no nested/infinite loops, whitelisted imports) → sandboxed execution
   (forkserver child, timeout) → NaN ≤30% / ≥5 distinct values per day → **temporal leakage unit test**
   (recompute on truncated history; any change = leakage) → LLM Judge. Failures go to Code Repair /
   Logic Improvement up to `max_repairs`. Deviation: paper judges before executing; we execute first to
   save quota.
3. Fitness on the train split: IC, RankIC, ICIR, RankICIR (abs values), MI. Qualified = all 5 ≥ 65th pct
   and floors; elite = ≥ 80th pct. Elites accumulate into the final pool; top 2 carried forward.
4. Adaptive generation: 2 valid + 2 worst factors summarised by LLM → injected into next prompts.
5. Thinking evolution: mutation / crossover / crossover→mutation children; fresh agent factors every 2 gens.
6. Final (`cogalpha/final.py`): LightGBM (or Ridge) on elite factors, trained on train, early-stopped on
   valid, scored on test (2023–2025) + TopK-Dropout (10/2) portfolio vs equal-weight universe, 10 bps.
   Always compared with a 6-factor classic baseline (momentum, reversal, vol, volume ratio, range, close pos).

Known calibration differences: MI floor set to 0 (paper 0.02 — our kNN MI on daily ranks is ~0–0.01);
paper scale (80 initial / 32 parents / 96 children / 24 gens / 21 agents on gpt-oss-120b, H100) is far
beyond Pro — configs are scaled down. No temperature control through `claude -p`.

## Reference numbers
- Classic baseline, test 2023–2025: IC 0.041, RankIC 0.029, ICIR 0.22, AER 9.7%, IR 0.63.
- Paper (CSI300, 10d): CogAlpha IC 0.059, RankIC 0.081, IR 1.90.
- Random signal loses ~8%/yr AER purely to turnover cost (sanity check).
