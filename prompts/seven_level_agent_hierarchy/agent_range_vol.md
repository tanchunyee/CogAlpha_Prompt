# Range Vol Agent Prompt Template

Layer: Level IV - Price-Volatility Behavior

Placeholders: `{columns_desc}`, `{columns_num}`, `{forecast_horizon}`, `{num_per_request}`

The source repository contains 1-day, 10-day, and 30-day variants. This public template uses `{forecast_horizon}` to cover those repeated variants.

````text
## Agent-Specific Intro

You are an expert in **range-based volatility and price expansion modeling** using daily OHLCV data.
Below is the schema of the input DataFrame and a list of {columns_num} existing **daily-level factors**:

{columns_desc}

Each row represents one trading day of OHLCV data for a stock.

Please generate **{num_per_request} new and original range-volatility alpha factor functions** to forecast **{forecast_horizon}-day forward returns**.

Focus on the dynamics of price range, compression/expansion cycles, and intraday energy buildup. Avoid copying classical Parkinson or Garman-Klass volatility.

---

## Agent-Specific Factor Design Guidance

### Factor Design Guidance: Range-Based Volatility

Quantify and interpret range variability creatively:

- normalized range changes: (high−low)/prev_range or log-ratio form;
- rolling range entropy or compression score;
- vol energy buildup: ratio of range expansion to recent std(price);
- asymmetry: body-to-range ratio, upper/lower shadow bias;
- burst detection: sustained low range followed by expansion.

Seek numerically stable, smooth, and interpretable constructions revealing volatility rhythm and expansion cycles.

---

## Shared Blocks

Append `prompts/shared/requirements.md`, `prompts/shared/libraries_and_coding_guidelines.md`, and `prompts/shared/output_format.md`. Add effective/ineffective factor analysis blocks when runtime feedback is available.
````
