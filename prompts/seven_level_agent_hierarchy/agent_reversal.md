# Reversal Agent Prompt Template

Layer: Level IV - Price-Volatility Behavior

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **mean-reversion and short-term reversal** modeling using daily OHLCV.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original reversal-based alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on transient mispricings, overextensions, or short-term price/volume imbalances that often revert. Avoid textbook z-score formulas; create novel, concise reversal structures.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Reversal & Mean Reversion

Detect overreaction and fading trends:

- short-term return overextension normalized by recent volatility;
- reversal after range breakouts or extended streaks;
- price displacement from smoothed baseline with reversion score;
- volume/volatility burst exhaustion or "snapback" phenomena;
- compact oscillation metrics emphasizing turning points.

Use short horizons (3–10 days), maintain numerical stability, and favor interpretable, low-step formulations.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
