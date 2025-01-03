import os
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic
import click

def get_llm_response(prompt: str, model: Optional[str] = None) -> Dict[Any, Any]:
    """Get response from LLM API"""
    if not model:
        model = "claude-3-sonnet-20240229"
        
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise click.ClickException("ANTHROPIC_API_KEY environment variable not set")
        
    client = Anthropic(api_key=api_key)
    
    try:
        message = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0.7,
            system="You are an expert panel coordinator helping to analyze complex topics.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse JSON from response
        response_text = message.content[0].text
        return json.loads(response_text)
        
    except Exception as e:
        raise click.ClickException(f"Error getting LLM response: {str(e)}")
