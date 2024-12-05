from pathlib import Path
from typing import Dict
import xml.etree.ElementTree as ET

from .state import WorkflowState
from ai.prompts import load_prompt_template, format_prompt
from ai.claude import query_claude

def run_observation(
    state: WorkflowState,
    cloud_config: Dict
) -> str:
    """Run initial observation stage"""
    print("[👀] Starting observation phase...")
    
    # Load statement
    statement = (state.decision_dir / "Statement.md").read_text()
    
    # Load and format prompts
    prompts = load_prompt_template(state.stage.value)
    system_prompt = format_prompt(prompts.system, state.context)
    user_prompt = format_prompt(prompts.user, {
        "FOUNDER_SITUATION": statement
    })
    
    # Query Claude
    response = await query_claude(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_key=cloud_config["claude_key"]
    )
    
    # Save observation
    observation_path = state.decision_dir / "Observation.xml"
    observation_path.write_text(response.content)
    
    print("[✅] Observation complete")
    return response.content
