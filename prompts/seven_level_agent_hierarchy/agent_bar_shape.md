# Bar Shape Agent Prompt Template

Layer: Level VII - Geometric and Fusion

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **candlestick geometry and bar-shape pattern analysis** using daily factors.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Please generate **{num_per_request} new and original bar-shape-based alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on extracting compact numerical representations of candle geometry, body symmetry, and shadow relationships.
Avoid simple pattern labeling; design continuous and interpretable shape metrics.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Bar Shape & Geometry

Translate candle geometry into quantitative signals:

- ratios: (close−open)/(high−low), (high−close)/(close−low), etc.;
- shadow asymmetry or balance indicators;
- body-to-range normalization and persistence over recent days;
- rolling geometry stability or asymmetry;
- short-run shape momentum: recent trend in candle proportions.

Encourage creativity and interpretability: derive smooth, bounded, differentiable functions using existing factors.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
