# Regime Gating Agent Prompt Template

Layer: Level VI - Stability and Regime-Gating

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **regime gating and adaptive signal activation** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original regime-gating alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Your goal is to model conditional activation of signals — where factor strength or relevance depends on volatility, trend, or liquidity regime.
Avoid static filters; instead, design adaptive gates that dynamically scale or modulate factor sensitivity based on regime changes.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Regime Gating Mechanisms

Discover simple yet powerful gating functions that adapt to market conditions:

- volatility-sensitive gating: scale signal intensity by normalized volatility level;
- trend-aware gating: activate only when directional persistence exceeds a threshold;
- liquidity gating: suppress signal under extremely low volume;
- asymmetric gating: respond differently in bullish vs bearish microstates;
- soft transitions: use continuous scaling (sigmoid/tanh) to ensure smooth adaptability.

Encourage creative activation designs: compact functions that turn existing OHLCV-derived signals “on/off” depending on state context, without relying on future data.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
