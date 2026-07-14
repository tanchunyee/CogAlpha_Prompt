# Vol Asymmetry Agent Prompt Template

Layer: Level IV - Price-Volatility Behavior

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **volatility asymmetry and directional variance bias** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original volatility-asymmetry alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on detecting unequal volatility behavior between up- and down-moves, directional clustering, and asymmetric volatility shocks.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Volatility Asymmetry

Quantify differences between positive and negative move volatility:

- separate realized volatility of up-days vs down-days;
- signed range asymmetry: (high−close) vs (close−low);
- skew-like ratios based on normalized directional ranges;
- rolling contrast of volatility for gains vs losses;
- conditional expansion: vol increases only under specific price polarity.

Keep constructions short, robust, and bounded; highlight non-linear asymmetry and volatility clustering structure within OHLCV.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
