from typing import Dict, Optional, Any
import os
from dataclasses import dataclass

@dataclass
class CloudConfig:
    claude_key: str
    openai_key: str
    model: str = "claude-2"

def init_cloud() -> CloudConfig:
    """Load API keys from environment"""
    return CloudConfig(
        claude_key=os.environ["ANTHROPIC_API_KEY"],
        openai_key=os.environ["OPENAI_API_KEY"]
    )

async def ask_claude(
    system_prompt: str, 
    user_prompt: str, 
    context: Dict[str, Any]
) -> str:
    """Send prompt to Claude and get response"""
    # Implementation here
    return "response"
