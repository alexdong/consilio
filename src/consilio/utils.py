import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai
import click
from consilio.models import Topic


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
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 1.0,
    response_definition: Optional[str] = None,
) -> Dict[Any, Any]:
    """Get response from LLM API

    Args:
        prompt: The prompt to send to the LLM
        system_prompt: Optional system prompt to set context (defaults to expert panel coordinator)
        model: Optional model name to use (defaults to config)
        temperature: Controls randomness in the response (0.0-1.0, default 1.0)
        response_definition: Optional JSON schema or description of expected response format
    """
    config = Topic.load().config
    model = model or config.model
    logger = logging.getLogger("consilio.llm")
    logger.debug(f"Getting LLM response with model: {model}")
    logger.debug(f"Prompt length: {len(prompt)} chars")
    logger.debug(f"Making API call to {model if model else 'default model'}")
    logger.debug(f"System prompt: {system_prompt}")
    logger.debug(f"User prompt: {prompt}")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise click.ClickException("GOOGLE_API_KEY environment variable not set")

    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Build complete prompt with response definition if provided
    full_prompt = f"{system_prompt}\n\n"
    if response_definition:
        full_prompt += f"Expected Response Format:\n{response_definition}\n\n"
    full_prompt += prompt

    response = genai.GenerativeModel(
        model, generation_config=generation_config  # type: ignore
    ).generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    logger.debug(f"Response: {response}")
    return json.loads(response.text)
