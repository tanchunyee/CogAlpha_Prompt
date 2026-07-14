# Herding Agent Prompt Template

Layer: Level V - Multi-Scale Complexity

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **herding behavior and crowding pattern modeling** using daily factors.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Please generate **{num_per_request} new and original herding-behavior alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on identifying collective, synchronous market reactions or overcrowded directional alignment inferred from existing factors.
Avoid literal “investor sentiment” proxies; instead, express herding via statistical convergence or one-sided participation dynamics.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Herding & Crowding Behavior

Quantify alignment and overconcentration effects:

- crowding intensity: ratio of directional persistence to volatility dispersion;
- participation imbalance: sustained same-sign momentum + volume clustering;
- autocorrelation of signed returns as proxy for synchronized trading;
- volatility narrowing during uniform directional flows;
- deherding bursts: abrupt transition from tight to dispersed movement.

Encourage conceptual depth: translate collective behavior into numerical proxies for crowding, overreaction, or premature consensus — all inferred from existing factors.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
