# Composite Agent Prompt Template

Layer: Level VII - Geometric and Fusion

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **composite factor construction and information fusion** using existing features.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Please generate **{num_per_request} new and original composite alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on blending multiple independent signals into coherent composites — emphasize synergy, de-noising, and orthogonalization.
Avoid simple linear averages or sums.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Composite Alpha Construction

Fuse signals through structured, interpretable transformations:

- weighted or volatility-adjusted averages of trend, volume, and range features;
- orthogonal combination: remove redundancy, amplify orthogonal content;
- regime-weighted composites: dynamic weights based on volatility or liquidity states;
- robust normalization before fusion (z-score or rank-scaling);
- include non-linear combination terms (e.g., product, ratio) but keep compact.

Strive for elegant, minimal composite forms with complementary subcomponents and clear economic intuition.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
