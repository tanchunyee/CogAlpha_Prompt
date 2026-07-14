# Output Format

Placeholders: None

````text
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
