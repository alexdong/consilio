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
    clarification_file = topic.directory / "clarification.md"
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
            click.echo(f"\n{i}. {q}")
        
        click.echo("\nPress Ctrl+D when finished.\n")
        answers = click.get_text_stream("stdin").read().strip()
        
        if answers:
            answers_file = topic.directory / "clarification_answers.md"
            answers_file.write_text(answers)
            click.echo(f"\nAnswers saved to: {answers_file}")
        
    except Exception as e:
        raise click.ClickException(f"Error getting clarification: {str(e)}")


def handle_clarify_command() -> None:
    """Main handler for the clarify command"""
    topic = Topic.load()
    get_clarification(topic)
