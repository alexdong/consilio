import json
import logging
import click
from typing import Dict, Any
from .models import Topic
from .utils import get_llm_response, render_template


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
    prompt = render_template("clarify.j2", topic=topic)
    system_prompt = render_template("system.j2")

    try:
        clarification = get_llm_response(prompt, system_prompt=system_prompt)
        save_clarification(topic, clarification)

        # Display questions for user
        click.echo("\nPlease provide answers to these clarifying questions:")
        for i, q in enumerate(clarification.get("questions", []), 1):
            click.echo(f"{i}. {q}")

    except Exception as e:
        raise click.ClickException(f"Error getting clarification: {str(e)}")


def handle_clarify_command() -> None:
    """Main handler for the clarify command"""
    topic = Topic.load()
    get_clarification(topic)
