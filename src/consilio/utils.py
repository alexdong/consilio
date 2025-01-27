import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

from google import genai
from google.genai import types

from typing import Optional
import click


def render_template(template_name: str, **kwargs: Any) -> str:
    """Render a Jinja2 template with the given context"""
    templates_dir = Path(__file__).parent / "prompts"
    env = Environment(
        loader=FileSystemLoader(templates_dir), autoescape=select_autoescape()
    )
    template = env.get_template(template_name)
    return template.render(**kwargs)


def get_llm_response(
    prompt: str,
    response_definition: Optional[Any] = None,
    temperature: float = 1.0,
) -> Dict[Any, Any]:
    """Get response from LLM API

    Args:
        prompt: The prompt to send to the LLM
        system_prompt: Optional system prompt to set context (defaults to expert panel coordinator)
        model: Optional model name to use (defaults to config)
        temperature: Controls randomness in the response (0.0-1.0, default 1.0)
        response_definition: Optional JSON schema or description of expected response format
    """
    logger = logging.getLogger("consilio.utils")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise click.ClickException("GOOGLE_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)

    system_prompt = render_template("system.j2")
    logger.debug(f"System prompt: {system_prompt}")
    logger.debug(f"User prompt: {prompt}")

    response = client.models.generate_content(
        # model="gemini-2.0-flash-thinking-exp-01-21",
        model="gemini-2.0-flash-exp",
        contents=types.Part.from_text(prompt),
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            response_mime_type="application/json",
            response_schema=response_definition,
        ),
    )
    logger.debug(f"Response: {response.text}")
    return json.loads(response.text)  # type: ignore
