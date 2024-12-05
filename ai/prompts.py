from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

@dataclass
class PromptTemplate:
    system: str
    user: str

def load_prompt_template(stage: str) -> PromptTemplate:
    """Load system and user prompts for a given stage"""
    base_path = Path("Prompts") / stage
    
    system = (base_path / "SystemPrompt.md").read_text()
    user = (base_path / "UserPrompt.md").read_text()
    
    return PromptTemplate(system=system, user=user)

def format_prompt(template: str, context: Dict[str, str]) -> str:
    """Format prompt template with context variables"""
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}"
        template = template.replace(placeholder, value)
    return template
