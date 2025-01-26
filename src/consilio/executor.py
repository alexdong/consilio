import logging
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar
import json
import click
from consilio.models import Topic, BaseModel
from consilio.utils import get_llm_response

T = TypeVar('T', bound=BaseModel)

def save_response(response: Any, file: Path) -> None:
    """Generic response saver for model objects"""
    json_str = json.dumps([r.model_dump() for r in response], indent=2)
    file.write_text(json_str)

def execute(
    topic: Topic,
    user_input_filepath: Optional[Path],
    user_input_template: str,
    build_prompt_fn: Callable[[Topic, str], str],
    response_definition: Optional[Any],
    response_filepath: Path,
    display_fn: Callable[..., None],
) -> None:
    logger = logging.getLogger("consilio.executor")

    user_input = ""
    if user_input_filepath:
        if user_input_filepath.exists():
            user_input = user_input_filepath.read_text()
        else:
            user_input = click.edit(text=user_input_template) # type: ignore
            assert user_input is not None
            user_input_filepath.write_text(user_input)
    logger.debug(f"User input saved to: {user_input_filepath}")

    prompt = build_prompt_fn(topic, user_input)
    logger.debug(f"Prompt generated: {prompt}")

    response = get_llm_response(prompt, response_definition)
    logger.debug(f"Response generated: {response}")
    
    save_response(response, response_filepath)
    logger.debug(f"Generated response saved to: {response_filepath}")

    display_fn(response)
