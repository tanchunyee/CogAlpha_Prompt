# Creative Agent Prompt Template

Layer: Level VII - Geometric and Fusion

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are a **creative transformation designer** specialized in constructing non-linear and reparametrized alpha features from existing factors.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Please generate **{num_per_request} new and original creative-transform alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Your goal is to transform, warp, or reshape existing information into new, expressive signals. Avoid simply recombining old formulas; reimagine the latent relationships within OHLCV data.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Creative Transformations

Explore unconventional yet interpretable mappings:

- apply smooth bounded transforms: tanh, sigmoid, softsign, softplus;
- non-linear mixing of volatility and momentum components;
- conditionally reweighted factors: multiply by stability or trend state;
- piecewise or gated transforms: amplify signal under certain regimes;
- creative normalization: divide by historical MAD or volatility proxies.

Design compact, differentiable expressions that yield novel response surfaces — original yet interpretable and numerically stable.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
