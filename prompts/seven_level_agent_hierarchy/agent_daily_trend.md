# Daily Trend Agent Prompt Template

Layer: Level IV - Price-Volatility Behavior

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **daily trend and momentum persistence modeling** using OHLCV time series.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

The input DataFrame consists of **daily aggregated OHLCV data** — each row represents a single trading day's features for a given stock.

Please generate **{num_per_request} new and original daily-trend-based alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on multi-day directional strength, momentum decay, and trend exhaustion. Avoid standard indicators; instead, invent compact, interpretable forms of persistence and continuation.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Daily Trend & Momentum

Explore sustained movement or directional consistency:

- multi-day momentum ratios (e.g., rolling cumulative return strength);
- trend acceleration or deceleration using short- vs long-window returns;
- persistence indicators: streak length, EMA of direction_sign;
- momentum exhaustion or saturation detection (trend weakening);
- normalized relative strength of trend to volatility.

Encourage originality — define novel persistence forms, smooth transitions, or asymmetric responses that differ from basic MA-cross ideas.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
