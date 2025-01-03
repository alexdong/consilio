import os
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai
import click
from .models import Config


def get_llm_response(prompt: str, model: Optional[str] = None, temperature: float = 1.0) -> Dict[Any, Any]:
    """Get response from LLM API
    
    Args:
        prompt: The prompt to send to the LLM
        model: Optional model name to use (defaults to config)
        temperature: Controls randomness in the response (0.0-1.0, default 0.7)
    """
    config = Config()
    if not model:
        model = config.data["model"]

    system_prompt = (
        "You are an expert panel coordinator helping to analyze complex topics."
    )

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
    return json.loads(message.content[0].text)


def _get_openai_response(prompt: str, model: str, system_prompt: str, temperature: float) -> Dict[Any, Any]:
    """Get response from OpenAI's GPT models"""
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
    return json.loads(response.choices[0].message.content)


def _get_gemini_response(prompt: str, model: str, system_prompt: str, temperature: float) -> Dict[Any, Any]:
    """Get response from Google's Gemini models"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise click.ClickException("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        f"{system_prompt}\n\n{prompt}",
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    return json.loads(response.text)
