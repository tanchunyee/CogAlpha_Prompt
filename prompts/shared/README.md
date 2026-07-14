# Shared Prompt Blocks

Shared prompt blocks define reusable instructions used by CogAlpha's generation and repair prompts. They keep factor-generation prompts consistent across agents and forecast horizons.

## Components

- **System and helper prompts** describe the general role of the LLM and support column-description or guidance-paraphrase tasks.
- **Requirements and output format** specify the expected factor-function structure, naming rules, index behavior, and response format.
- **Library and coding guidelines** define available Python libraries and implementation constraints for stable factor code.
- **Factor-guidance blocks** provide the common baseline factor-design principles reused by task-specific agents.
- **Feedback-analysis blocks** summarize effective and ineffective factors so later generations can reuse successful patterns and avoid repeated failures.

These blocks are assembled with task-specific agent prompts during generation.

## Usage

- `system_message.md` is used as the system message for LLM calls.
- `column_description.md` is an auxiliary prompt for turning raw factor/column names into concise descriptions before filling `{columns_desc}`.
- `effective_factor_summary.md` and `ineffective_factor_summary.md` summarize prior factor examples into compact feedback text.
- `effective_factor_analysis.md` and `ineffective_factor_analysis.md` wrap those summaries for insertion into a generation prompt.
- `requirements.md`, `libraries_and_coding_guidelines.md`, and `output_format.md` are appended to seven-level generation prompts.
- `guidance_paraphrase.md` can optionally rewrite an agent-specific factor-design guidance block before final prompt assembly.

## Templates

| Prompt Block | Template |
| --- | --- |
| Base Factor Guidance | `base_factor_guidance.md` |
| Column Description | `column_description.md` |
| Effective Factor Analysis | `effective_factor_analysis.md` |
| Effective Factor Summary | `effective_factor_summary.md` |
| Guidance Paraphrase | `guidance_paraphrase.md` |
| Ineffective Factor Analysis | `ineffective_factor_analysis.md` |
| Ineffective Factor Summary | `ineffective_factor_summary.md` |
| Libraries and Coding Guidelines | `libraries_and_coding_guidelines.md` |
| Output Format | `output_format.md` |
| Requirements | `requirements.md` |
| System Message | `system_message.md` |
