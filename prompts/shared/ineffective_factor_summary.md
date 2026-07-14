# Ineffective Factor Summary

Placeholders: None

````text
You are given several factor functions in the format:
            <<factor N>>
            State: low_metrics / dependent / unstable
            Metrics: IC / RankIC / ICIR / RankICIR
            Code: 
            <<function N>>
                def <factor_name>(df):
                    """Explain the logic. One clear idea. Short formula. No redundant stacking."""
                    df_copy = df.copy()
                    # factor computation
                    return df_copy['<factor_name>']
            <</function N>>
            <</factor N>>

            You are tasked with analyzing the given financial factors. For each factor, provide the following in a clear and structured format:
            1. **One Clear Idea**: one sentence stating the core intuition only.
            2. **Short Formula**: a single one-line math/pseudocode expression in backticks that represents the factor (no comments, no extra code)
            3. **Failure Analysis**: Identify potential issues or reasons why the factor might fail or be ineffective in its current design. Explain in one sentence why the factor would not perform well in real-world financial models or why it might not produce reliable results.
            IMPORTANT: Do not modify the factor names or codes in any way. Use the exact same name as input.
            Return your answer in the following format:
            <factor_name>:
                **One Clear Idea**: <description>
                **Short Formula**: `<one-line formula>`
                **Failure Analysis**: <analysis>

{', '.join(random.sample(factors_content, min(8, len(factors_content))))}
````
