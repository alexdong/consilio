from dataclasses import dataclass
from jinja2 import Template
from pathlib import Path
from typing import Dict


@dataclass
class PromptTemplate:
    system: str
    user: str


def load_prompt_template(stage: str) -> PromptTemplate:
    """Load system and user prompts for a given stage"""
    base_path = Path("Prompts")
    system = (base_path / "SystemPrompt.md").read_text()
    user = (base_path / f"UserPrompt-{stage}.md").read_text()
    return PromptTemplate(system=system, user=user)


def render_prompt(template_str: str, context: Dict[str, str]) -> str:
    """Use Jinja2 template to replace placeholders with context values"""
    template = Template(template_str)
    return template.render(context)
