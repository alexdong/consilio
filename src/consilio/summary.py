import logging
from dataclasses import dataclass
from typing import List
import click
from .models import Topic, Summary
from .utils import get_llm_response, render_template


@dataclass
class Round:
    number: int
    input: str
    response: str


def handle_summary_command() -> None:
    """Generate a summary of all discussion rounds"""
    logger = logging.getLogger("consilio.summary")
    logger.info("Generating discussion summary")
    topic = Topic.load()
    if not topic.discussion_file.exists():
        click.echo("No discussion file found.")
        return

    rounds: List[Round] = []

    # Gather all rounds
    current_round = 1
    while True:
        input_file = topic.discussion_input_file(current_round)
        response_file = topic.discussion_response_file(current_round)

        if not input_file.exists() or not response_file.exists():
            break

        rounds.append(
            Round(
                number=current_round,
                input=input_file.read_text(),
                response=response_file.read_text(),
            )
        )
        current_round += 1

    if not rounds:
        click.echo("No discussion rounds found.")
        return

    # Generate summary using template
    prompt = render_template("summary.j2", topic=topic, rounds=rounds)
    summary = Summary.model_validate(
        get_llm_response(prompt, response_definition=Summary)
    )

    # Save summary
    summary_file = topic.directory / "summary.json"
    summary_file.write_text(summary.model_dump_json(indent=2))
    click.echo(f"Summary generated and saved to: {summary_file}")
