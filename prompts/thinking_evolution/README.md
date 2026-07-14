# Thinking Evolution

Thinking Evolution contains prompts for evolving alpha-factor ideas across generations. These prompts help CogAlpha explore new candidates by modifying individual factors or recombining multiple factor ideas.

## Components

- **Mutation Agent** creates a new variant of an existing factor by changing its logic, transformation, window, or market interpretation.
- **Crossover Agent** combines useful ideas from multiple factors into a new candidate while avoiding direct duplication.

Together, these prompts support iterative search over code-based alpha factors.

## Usage

Use `prompts/shared/system_message.md` as the system message. Each evolution template is a complete user prompt:

- `mutation_agent.md`: fill `{intro}`, `{extra_guidance}`, and `{original_factor_code}`.
- `crossover_agent.md`: fill `{intro}`, `{extra_guidance}`, `{parent_factor_1_code}`, and `{parent_factor_2_code}`.

`{intro}` should describe the available columns and the factor-generation task. `{extra_guidance}` can contain the active agent theme, successful/failed factor feedback, or other mechanism-specific guidance.

## Templates

| Agent | Template |
| --- | --- |
| Mutation Agent | `mutation_agent.md` |
| Crossover Agent | `crossover_agent.md` |
