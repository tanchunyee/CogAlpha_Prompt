# Stability Agent Prompt Template

Layer: Level VI - Stability and Regime-Gating

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **signal and return stability analysis** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original stability-based alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on persistence, noise filtering, and robustness of price dynamics.
Avoid trivial variance measures; instead, quantify temporal consistency and structural smoothness of returns, ranges, or derived signals.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Temporal Stability & Consistency

Build measures of predictability, continuity, or resilience:

- rolling variance ratio between short-term and long-term windows;
- trend or volatility “smoothness” (ratio of mean to std of incremental changes);
- sign-change frequency (directional stability index);
- volatility-of-volatility (metavolatility) decay;
- normalized stability metrics emphasizing steady vs chaotic behavior.

Encourage interpretability and numerical robustness: define compact indicators that express whether the underlying dynamics are stable, persistent, or erratic — all using only OHLCV inputs.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
