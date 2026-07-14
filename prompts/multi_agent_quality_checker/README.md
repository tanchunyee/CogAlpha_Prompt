# Multi-Agent Quality Checker

The multi-agent quality checker improves the reliability of generated factor code after initial generation. These prompts inspect code quality, repair execution failures, judge whether a factor is logically valid, and propose targeted improvements.

## Components

- **Code Quality Agent** reviews generated factor code for correctness, readability, robustness, and compliance with prompt constraints.
- **Code Repair Agent** fixes runtime or syntax failures while preserving the original factor intent.
- **Judge Agent** evaluates whether a generated factor is meaningful, executable, and aligned with the expected alpha-mining task.
- **Logic Improvement Agent** rewrites weak or under-specified factor logic into a clearer and more financially grounded version.

## Usage

Use `prompts/shared/system_message.md` as the system message. Each quality-checker template is a complete user prompt:

- `code_quality_agent.md`: fill `{code}` with one candidate factor function.
- `code_repair_agent.md`: fill `{columns_num}`, `{columns_desc}`, `{old_code}`, and `{error}` after a factor fails execution.
- `judge_agent.md`: fill the candidate factor and the requested judgment context.
- `logic_improvement_agent.md`: fill the factor logic or code that should be improved.

These prompts are usually run after a generation or evolution step, before accepting a factor into later evaluation.

## Templates

| Agent | Template |
| --- | --- |
| Code Quality Agent | `code_quality_agent.md` |
| Code Repair Agent | `code_repair_agent.md` |
| Judge Agent | `judge_agent.md` |
| Logic Improvement Agent | `logic_improvement_agent.md` |
