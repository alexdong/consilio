import os
from typing import Dict, Optional
import anthropic
from dataclasses import dataclass


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
    # print(message)
    content = "".join(block.text for block in message.content if block.type == "text")
    return ClaudeResponse(content=content, raw=message.model_dump())


if __name__ == "__main__":
    response = query_claude(
        system_prompt="Hello, I'm a bot. What's your name?",
        user_prompt="My name is Alice.",
        assistant="It's good",
        temperature=0.9,
    )
    print(response.raw)
