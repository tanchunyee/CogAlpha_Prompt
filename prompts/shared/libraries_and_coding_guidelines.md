# Libraries And Coding Guidelines

Placeholders: None

````text
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
````
