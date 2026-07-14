# Order Imbalance Agent Prompt Template

Layer: Level III - Price-Volume Dynamics

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **order-imbalance and directional pressure** modeling using daily OHLCV (no L2, no VWAP).
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

The input DataFrame consists of **daily aggregated OHLCV data** — each row represents a single trading day's features for a given stock.

Please generate **{num_per_request} new and original order-imbalance alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Think in terms of one-sided participation and pressure persistence inferred from price direction and activity proxies. Keep designs compact and robust.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Directional Pressure from OHLCV

Infer buy/sell pressure without microstructure feeds:

- direction × intensity: couple return or (close−open) with standardized volume/turnover;
- gap-informed pressure: relate overnight direction to same-day activity and close location-in-range;
- persistence & decay: smoothed imbalance streaks and their fading profile;
- asymmetry: treat positive vs negative pressure differently when ranges are compressed/expanded;
- guardrails: normalize by range or price·volume scale; apply soft bounding only if necessary.

Prioritize interpretability and stability; keep to 1–3 coherent steps per factor, using OHLCV only.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
