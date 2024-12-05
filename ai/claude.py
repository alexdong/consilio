from typing import Dict, Optional
import anthropic
from dataclasses import dataclass

@dataclass
class ClaudeResponse:
    content: str
    raw: Dict  # Store raw API response

def query_claude(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    model: str = "claude-2",
    temperature: float = 0.7
) -> ClaudeResponse:
    """Send query to Claude and get response"""
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=temperature
    )
    
    return ClaudeResponse(
        content=message.content[0].text,
        raw=message.model_dump()
    )
