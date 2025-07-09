import json
import logging
import os
from pathlib import Path
from typing import Any

import click
from google import genai
from google.genai import types
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_template(template_name: str, **kwargs: Any) -> str:  # noqa: ANN401
    """Render a Jinja2 template with the given context"""
    templates_dir = Path(__file__).parent / "prompts"
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(),
    )
    template = env.get_template(template_name)
    return template.render(**kwargs)


def get_llm_response(
    prompt: str,
    response_definition: type | None = None,
    temperature: float = 1.0,
) -> dict[str, str | list | dict]:
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
        msg = "GOOGLE_API_KEY environment variable not set"
        raise click.ClickException(msg)
    client = genai.Client(api_key=api_key)

    system_prompt = render_template("system.j2")
    logger.debug("System prompt: %s", system_prompt)
    logger.debug("User prompt: %s", prompt)

    config_args = {
        "system_instruction": system_prompt,
        "temperature": temperature,
        "response_mime_type": "application/json",
    }
    if response_definition is not None:
        config_args["response_schema"] = response_definition

    config = types.GenerateContentConfig(**config_args)
    response = client.models.generate_content(
        # model="gemini-2.0-flash-thinking-exp-01-21",
        model="gemini-2.0-pro-exp-02-05",
        contents=[types.Part(text=prompt)],
        config=config,
    )
    logger.debug("Response: %s", response.text)
    return json.loads(response.text)  # type: ignore


if __name__ == "__main__":
    response = get_llm_response("")
    print(response)
