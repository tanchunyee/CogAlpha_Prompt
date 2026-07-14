# Requirements

Placeholders: None

````text
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
````
