import json
import logging
import click
import jsonschema
from pathlib import Path
from typing import Dict, Any
from .models import Topic
from .utils import get_llm_response, render_template


schema = (Path(__file__).parent / "schemas" / "clarification_schema.json").read_text()


def validate_clarification(clarification: Dict[Any, Any]) -> None:
    """Validate clarification against schema"""
    jsonschema.validate(instance=clarification, schema=json.loads(schema))


def save_clarification(topic: Topic, clarification: Dict[Any, Any]) -> None:
    """Save clarification response to file"""
    logger = logging.getLogger("consilio.clarify")
    logger.info("Saving clarification response")
    clarification_file = topic.clarification_answers_file
    clarification_file.write_text(json.dumps(clarification, indent=2))
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

        # Display questions for user
        click.echo("\nPlease provide answers to these clarifying questions:")
        for i, q in enumerate(clarification.get("questions", []), 1):
            click.echo(f"{i}. {q}")
            
        # Display missing context
        if missing_context := clarification.get("missing_context"):
            click.echo("\nMissing Context:")
            for item in missing_context:
                click.echo(f"• {item}")
                
        # Display assumptions
        if assumptions := clarification.get("assumptions"):
            click.echo("\nAssumptions to Verify:")
            for item in assumptions:
                click.echo(f"• {item}")
                
        # Display suggestions
        if suggestions := clarification.get("suggestions"):
            click.echo("\nSuggestions:")
            for item in suggestions:
                click.echo(f"• {item}")

    except Exception as e:
        raise click.ClickException(f"Error getting clarification: {str(e)}")


def handle_clarify_command() -> None:
    """Main handler for the clarify command"""
    topic = Topic.load()
    get_clarification(topic)
