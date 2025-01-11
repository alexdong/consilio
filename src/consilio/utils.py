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
) -> Dict[Any, Any]:
    """Get response from LLM API

    Args:
        prompt: The prompt to send to the LLM
        system_prompt: Optional system prompt to set context (defaults to expert panel coordinator)
        model: Optional model name to use (defaults to config)
        temperature: Controls randomness in the response (0.0-1.0, default 1.0)
    """
    config = Topic.load().config
    model = model or config.model
    logger = logging.getLogger("consilio.llm")
    logger.debug(f"Getting LLM response with model: {model}")
    logger.debug(f"Prompt length: {len(prompt)} chars")
    logger.info(f"Making API call to {model if model else 'default model'}")

    if system_prompt is None:
        system_prompt = (
            "You are an expert panel coordinator helping to analyze complex topics."
        )
    logger.debug(f"User prompt: {prompt}")
    logger.debug(f"System prompt: {system_prompt}")

    try:
        if "claude" in model:
            return _get_anthropic_response(prompt, model, system_prompt, temperature)
        elif "gpt" in model:
            return _get_openai_response(prompt, model, system_prompt, temperature)
        elif "gemini" in model:
            return _get_gemini_response(prompt, model, system_prompt, temperature)
        else:
            raise click.ClickException(f"Unsupported model: {model}")

    except Exception as e:
        raise click.ClickException(f"Error getting LLM response: {str(e)}")


def _get_anthropic_response(
    prompt: str, model: str, system_prompt: str, temperature: float
) -> Dict[Any, Any]:
    """Get response from Anthropic's Claude"""
    logger = logging.getLogger("consilio.llm.anthropic")
    logger.info("Making Anthropic API call")
    logger.debug(f"Using model: {model}, temperature: {temperature}")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise click.ClickException("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=2000,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    response = json.loads(message.content[0].text)  # type: ignore
    logger.debug(f"Response: {response}")
    return json.loads(response)


def _get_openai_response(
    prompt: str, model: str, system_prompt: str, temperature: float
) -> Dict[Any, Any]:
    """Get response from OpenAI's GPT models"""
    logger = logging.getLogger("consilio.llm.openai")
    logger.info("Making OpenAI API call")
    logger.debug(f"Using model: {model}, temperature: {temperature}")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    logger.debug(f"Response: {response.choices[0].message.content}")  # type: ignore
    return json.loads(response.choices[0].message.content)  # type: ignore


def _get_gemini_response(
    prompt: str, model: str, system_prompt: str, temperature: float
) -> Dict[Any, Any]:
    """Get response from Google's Gemini models"""
    logger = logging.getLogger("consilio.llm.gemini")
    logger.info("Making Gemini API call")
    logger.debug(f"Using model: {model}, temperature: {temperature}")
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
    response = genai.GenerativeModel(
        model, generation_config=generation_config  # type: ignore
    ).generate_content(
        f"{system_prompt}\n\n{prompt}",
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    logger.debug(f"Response: {response.text}")
    return json.loads(response.text)
