# Prompt Families

This directory organizes the public prompt templates used by CogAlpha into the main functional families described in the paper.

## Components

- [Seven-Level Agent Hierarchy](seven_level_agent_hierarchy/README.md): task-specific generation agents for different market mechanisms and alpha-design perspectives.
- [Multi-Agent Quality Checker](multi_agent_quality_checker/README.md): review, repair, judgment, and logic-improvement prompts for validating generated factor code.
- [Thinking Evolution](thinking_evolution/README.md): mutation and crossover prompts for evolving candidate factors across generations.
- [Shared Prompt Blocks](shared/README.md): common requirements, library rules, output format, feedback-analysis blocks, and helper prompts reused by generation agents.

See each family README for its template list.

## Assembly Overview

Use `shared/system_message.md` as the system message. Build the user message from one family:

- For new factor generation, combine a seven-level agent intro/guidance with shared requirement, library, and output-format blocks.
- For quality checking, use one multi-agent quality checker template and fill the code/error placeholders.
- For thinking evolution, use either mutation or crossover and fill the parent-factor placeholders plus any extra guidance.

Do not include local code paths or repository-specific metadata in assembled prompts.
