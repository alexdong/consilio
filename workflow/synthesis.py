from pathlib import Path
from typing import Dict

from .state import WorkflowState
from ai.prompts import load_prompt_template, format_prompt
from ai.claude import query_claude

def run_synthesis(
    state: WorkflowState,
    cloud_config: Dict
) -> str:
    """Run final synthesis stage"""
    print("[🧠] Starting synthesis phase...")
    
    # Load all previous content
    statement = (state.decision_dir / "Statement.md").read_text()
    observation = (state.decision_dir / "Observation.xml").read_text()
    perspectives = (state.decision_dir / "Perspectives.xml").read_text()
    
    # Load and format prompts
    prompts = load_prompt_template(state.stage.value)
    system_prompt = format_prompt(prompts.system, state.context)
    user_prompt = format_prompt(prompts.user, {
        "FOUNDER_SITUATION": statement,
        "ADVISOR_OBSERVATION": observation,
        "PERSPECTIVE_RESPONSE": perspectives
    })
    
    # Query Claude
    response = await query_claude(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_key=cloud_config["claude_key"]
    )
    
    # Save memo
    memo_path = state.decision_dir / "Memo.md"
    memo_path.write_text(response.content)
    
    print("[✅] Synthesis complete")
    return response.content
