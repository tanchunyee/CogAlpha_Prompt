# Liquidity Agent Prompt Template

Layer: Level III - Price-Volume Dynamics

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **liquidity and transaction-cost** modeling using daily OHLCV.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

The input DataFrame consists of **daily aggregated OHLCV data** — each row represents a single trading day's features for a given stock.

Please generate **{num_per_request} new and original liquidity-oriented alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Aim to reflect trading frictions, market depth, and price-impact sensitivity implied by OHLCV alone. Encourage creative, compact constructions rather than generic recipes.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Liquidity & Impact

Explore liquidity from multiple angles, combining price moves and activity:

- impact intuition: how much price movement occurs per unit of activity (volume or dollarized proxy);
- participation & crowding: turnover intensity, its variability, and persistence of thin/rich liquidity states;
- shock absorption: recovery speed of liquidity after spikes/dry-ups;
- scale & normalization: stabilize by price level/range and use gentle bounding (clip/tanh) only when needed;
- regime awareness (soft): let features respond differently in compressed vs expanded ranges.

Keep formulas short (1–3 steps), numerically safe (add ε where needed), and strictly OHLCV-based.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
