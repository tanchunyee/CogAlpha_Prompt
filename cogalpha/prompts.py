"""Load the repo's Markdown prompt templates and assemble them as the README describes."""
from __future__ import annotations

import re
from functools import cache
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
PARAPHRASE_STYLES = ["light", "moderate", "creative", "divergent", "concrete"]
# The summary templates end in a leftover Python f-string expression; we splice samples there.
_FSTRING_TAIL = re.compile(r"\{', '\.join\([^\n]*\)\}")


@cache
def template(rel: str) -> str:
    """Body of the ````text fence in prompts/<rel>.md."""
    text = (PROMPT_DIR / f"{rel}.md").read_text()
    m = re.search(r"````text\n(.*?)\n````", text, re.S)
    if not m:
        raise ValueError(f"no ````text block in {rel}")
    return m.group(1)


def fill(text: str, **values) -> str:
    """Placeholder substitution that leaves code braces alone (no str.format)."""
    for k, v in values.items():
        text = text.replace("{" + k + "}", str(v))
    return text


def system_message() -> str:
    return template("shared/system_message")


def agent_blocks(agent: str) -> tuple[str, str]:
    body = template(f"seven_level_agent_hierarchy/agent_{agent}")
    intro = body.split("## Agent-Specific Intro", 1)[1].split("## Agent-Specific Factor Design Guidance")[0]
    guidance = body.split("## Agent-Specific Factor Design Guidance", 1)[1].split("## Shared Blocks")[0]
    strip = lambda s: s.strip().removesuffix("---").strip()
    return strip(intro), strip(guidance)


def list_agents() -> list[str]:
    return sorted(p.stem.removeprefix("agent_")
                  for p in (PROMPT_DIR / "seven_level_agent_hierarchy").glob("agent_*.md"))


def agent_intro(agent: str, ctx: dict) -> str:
    return fill(agent_blocks(agent)[0], **ctx)


def generation_prompt(agent: str, ctx: dict, guidance: str | None = None,
                      effective_cot: str | None = None, ineffective_cot: str | None = None) -> str:
    intro, default_guidance = agent_blocks(agent)
    blocks = [fill(intro, **ctx)]
    if effective_cot:
        blocks.append(fill(template("shared/effective_factor_analysis"), effective_CoT=effective_cot))
    if ineffective_cot:
        blocks.append(fill(template("shared/ineffective_factor_analysis"), ineffective_CoT=ineffective_cot))
    blocks += [template("shared/requirements"), guidance or default_guidance,
               template("shared/libraries_and_coding_guidelines"), template("shared/output_format")]
    return "\n\n---\n\n".join(blocks)


def paraphrase_prompt(guidance: str, style: str) -> str:
    return fill(template("shared/guidance_paraphrase"), guidance=guidance, rewrite_style=style)


def feedback_block(guidance: str, effective_cot: str | None, ineffective_cot: str | None) -> str:
    """`{extra_guidance}` for the evolution agents: theme guidance + adaptive feedback."""
    parts = [guidance]
    if effective_cot:
        parts.append(fill(template("shared/effective_factor_analysis"), effective_CoT=effective_cot))
    if ineffective_cot:
        parts.append(fill(template("shared/ineffective_factor_analysis"), ineffective_CoT=ineffective_cot))
    return "\n\n".join(parts)


def mutation_prompt(intro: str, extra_guidance: str, code: str) -> str:
    return fill(template("thinking_evolution/mutation_agent"), intro=intro,
                extra_guidance=extra_guidance, original_factor_code=code)


def crossover_prompt(intro: str, extra_guidance: str, code1: str, code2: str) -> str:
    return fill(template("thinking_evolution/crossover_agent"), intro=intro, extra_guidance=extra_guidance,
                parent_factor_1_code=code1, parent_factor_2_code=code2)


def judge_prompt(code: str) -> str:
    return fill(template("multi_agent_quality_checker/judge_agent"), new_factor_code=code)


def code_quality_prompt(code: str) -> str:
    return fill(template("multi_agent_quality_checker/code_quality_agent"), code=code)


def repair_prompt(ctx: dict, code: str, error: str) -> str:
    return fill(template("multi_agent_quality_checker/code_repair_agent"),
                columns_num=ctx["columns_num"], columns_desc=ctx["columns_desc"], old_code=code, error=error)


def logic_improvement_prompt(ctx: dict, code: str, feedback: str) -> str:
    return fill(template("multi_agent_quality_checker/logic_improvement_agent"),
                columns_num=ctx["columns_num"], columns_desc=ctx["columns_desc"],
                old_code=code, dynamic_feedback=feedback)


def summary_prompt(kind: str, factor_blocks: list[str]) -> str:
    """kind: 'effective' | 'ineffective'. factor_blocks are pre-formatted <<factor N>> entries."""
    body = template(f"shared/{kind}_factor_summary")
    return _FSTRING_TAIL.sub(lambda _: "\n\n".join(factor_blocks), body)
