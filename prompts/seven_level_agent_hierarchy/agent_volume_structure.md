# Volume Structure Agent Prompt Template

Layer: Level III - Price-Volume Dynamics

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **volume structure and distribution dynamics** using daily OHLCV.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

The input DataFrame consists of **daily aggregated OHLCV data** — each row represents a single trading day's features for a given stock.

Please generate **{num_per_request} new and original volume-structure alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on shape, concentration, variability, and organization of volume over time (not price itself). Encourage creative, parsimonious formulations.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Volume Shape & Organization

Describe how trading activity is distributed and evolves:

- concentration vs dispersion: compact proxies for volume concentration, inequality, or clustering;
- burstiness: frequency and intensity of spikes relative to a robust baseline;
- asymmetry & tails: simple skew/kurtosis-style indicators with stabilization;
- multi-horizon organization: short vs long activity balance and its persistence;
- hygiene: robust scaling (median/IQR), gentle clipping when needed, and limited-step formulas.

Use OHLCV only; aim for interpretable, low-complexity functions that expose the structure and rhythm of participation.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
