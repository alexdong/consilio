import os
from typing import Dict, Optional
from pathlib import Path
import yaml
from dataclasses import dataclass
from jinja2 import Template
import anthropic

# XML Utils
def escape_xml_string(xml_string):
    # Common XML escapes
    replacements = {
        "&": "&amp;",
    }

    # Replace special characters with their escaped versions
    for char, escape in replacements.items():
        xml_string = xml_string.replace(char, escape)

    return xml_string.strip()

# Claude Integration
@dataclass
class ClaudeResponse:
    content: str
    raw: Dict  # Store raw API response

def query_claude(
    user_prompt: str,
    system_prompt: Optional[str] = None,
    assistant: Optional[str] = None,
    temperature: float = 0.7,
) -> ClaudeResponse:
    """Send query to Claude and get response"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=temperature,
        system=system_prompt if system_prompt else "",
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant}] if assistant else [],
            },
        ],
    )
    content = "".join(block.text for block in message.content if block.type == "text")
    return ClaudeResponse(content=content, raw=message.model_dump())

# Config Management
@dataclass 
class Context:
    domain: str
    perspective: str
    user_role: str

def load_context(config_path: Optional[Path] = None) -> Context:
    """Load context from yaml file"""
    if not config_path:
        config_path = Path(".consilio.yml")
    
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    return Context(**data)

# Prompt Management
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
