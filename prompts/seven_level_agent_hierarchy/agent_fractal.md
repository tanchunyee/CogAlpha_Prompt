# Fractal Agent Prompt Template

Layer: Level V - Multi-Scale Complexity

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **fractal and multi-scale complexity modeling** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original fractal-complexity alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on irregularity, scaling behavior, and long-memory structure in price dynamics. Avoid explicitly computing Hurst exponents; instead, find simple, differentiable proxies that express self-similarity or structural complexity.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Fractal & Multi-Scale Behavior

Derive compact proxies for complexity and persistence across scales:

- ratio of multi-window volatilities (short vs long horizon variability);
- variance-of-variance or volatility roughness score;
- local scaling slope between different rolling ranges or std windows;
- oscillation frequency: count of zero-crossings in detrended returns;
- persistence index: normalized cumulative sign-consistency.

Encourage creative constructs that summarize roughness, self-similarity, or temporal irregularity.
Use only OHLCV and simple rolling statistics; keep outputs stable and interpretable.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
