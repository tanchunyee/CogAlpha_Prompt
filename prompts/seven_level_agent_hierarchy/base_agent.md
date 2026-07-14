# Base Agent Prompt Template

Placeholders: `{columns_desc}`, `{columns_num}`, `{factor_type}`, `{num_per_request}`

This is the generic generation template. Task-specific agents replace the intro and factor-design guidance with their own versions.

````text
You are a senior quantitative factor engineer. Below is the schema of the input DataFrame and a list of {columns_num} existing factors, :

{columns_desc}

The input DataFrame consists of **daily aggregated factors** — i.e., each row represents a single trading day's features for a given stock, already aggregated to daily frequency.

Please generate **{num_per_request} new and original quantitative factor functions** that are different from existing ones. Each factor should be implemented as a complete Python function.

---

{{optional: include prompts/shared/effective_factor_analysis.md when effective factor feedback is available}}

---

{{optional: include prompts/shared/ineffective_factor_analysis.md when ineffective factor feedback is available}}

---

### Requirements:

- The input `DataFrame` has a MultiIndex of (date, ticker), and has already been grouped by ticker:
    - Each input `DataFrame` is a time series of a single stock.

- Output: A `pd.Series` indexed by `(date, ticker)` with the **same name** as the function.

- Each function must:
    - Have a descriptive, unique name: `factor_<logic>_<transformation(s)>_<window(s)>_<field>`.
    - Include a clear docstring explaining the logic and formula.
    - Balance predictive power with economic/financial interpretability.
    - The output column name must match the function name.
    - Be concise, precise, and readable.
    - Build new alpha factors based on existing ones.

---

### Factor Design Guidance:

You are encouraged to explore a wide variety of signals and techniques related to {factor_type}, including but not limited to:

- [List of common techniques / example categories]
- [List of possible interactions or advanced ideas]

Please do NOT limit yourself to simple formulas or common patterns.  
You are expected to innovate, introduce mathematically sophisticated or unconventional structures, and combine multiple concepts where reasonable.

The goal is to generate factors that are **predictive**, **robust**, and **economically interpretable**, while being **structurally diverse** from existing factors.

---

### Pre-imported libraries you can use (current versions):

- `"np"`: import numpy as np  (numpy version: 2.2.6)
- `"pd"`: import pandas as pd  (pandas version: 2.2.3)
- `"stats"`: from scipy import stats  (scipy version: 1.15.3)
- `"talib"`: import talib  (talib version: 0.5.1)
- `"math"`: import math  (built-in module)

Coding Guidelines:
- Ensure the code is robust, efficient, and optimized:
    - Handle edge cases and exceptions (e.g., NaN values).
    - Minimize unnecessary computations and prefer vectorized operations (e.g., pandas, numpy).
    - Ensure numerical stability.
    - **Strict Rule: Nested loops are absolutely forbidden.**
        - You must **never** write any form of loop inside another loop.
        - Forbidden patterns include but are not limited to:
            - `for` inside `for`
            - `while` inside `while`
            - `for` inside `while`
            - `while` inside `for`
        - Any nested iteration structure is **prohibited**, regardless of indentation depth.
        - The use of `while True` or any potentially infinite loop is **strictly prohibited**.
- When filtering or assigning values in a DataFrame, always use `df_copy.loc[row_indexer, col_indexer] = value`.

- Code should be clean, maintainable, and efficient for large datasets:
    - Use descriptive variable names and minimize memory usage.
    - Avoid creating unnecessary copies of large dataframes.

---

### Output format specification:

- Do NOT use markdown (like ```python)
- Do NOT add explanation or comments outside the function
- Each function must be wrapped inside: `<<function N>>` ... `<</function N>>`
- All generated code must be executable and numerically stable.
- Always define intermediate columns (e.g. df_copy['x']) before referencing them later.
- The returned Series **must be named exactly the same as the function name**.
- Each function should follow this format:

<<function N>>
def factor_xyz(df):
    """Explain the logic. One clear idea. Short formula. No redundant stacking."""
    df_copy = df.copy()
    # factor computation
    return df_copy['factor_xyz']
<</function N>>
````
