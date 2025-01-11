import json
import logging
import click
import jsonschema
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from .models import Topic, Clarification
from .utils import get_llm_response, render_template


schema = (Path(__file__).parent / "schemas" / "clarification_schema.json").read_text()


def display_clarification(clarification: Dict[Any, Any]) -> None:
    """Display clarification in markdown format using rich"""
    console = Console()

    # Convert to Clarification object if it's a dict
    if isinstance(clarification, dict):
        clarification = Clarification.from_dict(clarification)

    # Display using rich markdown
    console.print(Markdown(clarification.to_markdown()))


def validate_clarification(clarification: Dict[Any, Any]) -> None:
    """Validate clarification against schema"""
    jsonschema.validate(instance=clarification, schema=json.loads(schema))


def save_clarification(topic: Topic, clarification: Dict[Any, Any]) -> None:
    """Save clarification response to file"""
    logger = logging.getLogger("consilio.clarify")
    logger.info("Saving clarification response")
    clarification_file = topic.clarification_answers_file
    if isinstance(clarification, dict):
        clarification = Clarification.from_dict(clarification)
    clarification_file.write_text(json.dumps(clarification.to_json(), indent=2))
    click.echo(f"Clarification saved to: {clarification_file}")


def get_clarification(topic: Topic) -> None:
    """Get clarification questions and suggestions"""
    logger = logging.getLogger("consilio.clarify")
    logger.info("Getting clarification for topic")

    # Generate clarification using template
    prompt = render_template("clarify.j2", topic=topic, schema=schema)
    system_prompt = render_template("system.j2")

    try:
        clarification = get_llm_response(prompt, system_prompt=system_prompt)

        # Validate clarification against schema
        try:
            validate_clarification(clarification)
        except jsonschema.ValidationError as e:
            raise click.ClickException(
                f"Generated clarification failed validation: {str(e)}"
            )

        save_clarification(topic, clarification)

        # Display the clarification
        display_clarification(clarification)

    except Exception as e:
        raise click.ClickException(f"Error getting clarification: {str(e)}")


def handle_clarify_command() -> None:
    """Main handler for the clarify command"""
    topic = Topic.load()
    get_clarification(topic)
