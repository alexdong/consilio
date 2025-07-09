import json
import logging
from typing import Any

import click
from rich.console import Console
from rich.markdown import Markdown

from .models import Clarification, Topic
from .utils import get_llm_response, render_template


def display_clarification(clarification: dict[Any, Any]) -> None:
    """Display clarification in markdown format using rich"""
    console = Console()

    # Convert to Clarification object if it's a dict
    message = Clarification.model_validate(clarification).to_markdown()

    # Display using rich markdown
    console.print(Markdown(message))


def save_clarification(topic: Topic, clarification: dict[Any, Any]) -> None:
    """Save clarification response to file"""
    logger = logging.getLogger("consilio.clarify")
    logger.info("Saving clarification response")
    clarification_file = topic.clarification_answers_file
    clarification_file.write_text(
        json.dumps(Clarification.model_validate(clarification).to_json(), indent=2),
    )
    click.echo(f"Clarification saved to: {clarification_file}")


@click.command()
def clarify() -> None:
    """Get clarification questions and suggestions"""
    logger = logging.getLogger("consilio.clarify")
    logger.info("Getting clarification for topic")

    topic = Topic.load()

    # Generate clarification using template
    prompt = render_template("clarify.j2", topic=topic)

    try:
        clarification = get_llm_response(prompt, response_definition=Clarification)

        save_clarification(topic, clarification)

        # Display the clarification
        display_clarification(clarification)

    except Exception as e:
        raise click.ClickException(f"Error getting clarification: {e!s}")
