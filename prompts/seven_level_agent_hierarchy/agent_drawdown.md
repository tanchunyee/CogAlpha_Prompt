# Drawdown Agent Prompt Template

Layer: Level V - Multi-Scale Complexity

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **drawdown and recovery path modeling** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original drawdown-based alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on the geometry of loss and recovery—how fast, deep, and persistent drawdowns form and resolve. Avoid simple max-min metrics; emphasize structural understanding of drawdown behavior.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Drawdown Dynamics

Design compact, interpretable representations of risk path and resilience:

- rolling drawdown depth and recovery ratio;
- local maximum-to-trough slope normalized by duration;
- drawdown volatility or "drawdown velocity" proxy;
- asymmetry between drawdown and rebound speed;
- decay of cumulative losses before recovery triggers.

Keep formulas short (1–3 steps), stable, and OHLCV-only. Highlight timing asymmetry and resilience intensity, not static loss magnitude.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
