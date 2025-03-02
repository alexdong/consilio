import click
import logging
from typing import Any, Optional
from consilio.models import Topic, Discussion, display_interview
from consilio.utils import render_template
from consilio.perspective_utils import (
    select_perspective,
    get_most_recent_perspective,
    get_perspective,
)
from consilio.executor import execute


@click.group()
def interview():
    """Manage interviews with different perspectives"""
    pass


def _build_interview_prompt(
    topic: Topic,
    perspective: dict[Any, Any],
    perspective_index: int,
    round_num: int,
    user_input: str,
) -> str:
    """Build prompt for interview rounds"""
    logger = logging.getLogger("consilio.interview")
    logger.debug(
        f"Building interview prompt for perspective {perspective_index}, round {round_num}"
    )
    history = []

    # Add context from discussion rounds
    for i in range(1, topic.latest_discussion_round + 1):
        try:
            input_file = topic.discussion_input_file(i)
            response_file = topic.discussion_response_file(i)

            if input_file.exists():
                history.append(
                    f"Discussion Round {i} Input:\n{input_file.read_text()}\n"
                )
            if response_file.exists():
                history.append(
                    f"Discussion Round {i} Response:\n{response_file.read_text()}\n"
                )
        except Exception as e:
            click.echo(f"Warning: Error reading discussion round {i}: {str(e)}")

    # Add context from previous interview rounds
    interview_history = []
    for i in range(1, round_num):
        try:
            input_file = topic.interview_input_file(perspective_index, i)
            response_file = topic.interview_response_file(perspective_index, i)

            if input_file.exists():
                interview_history.append(
                    f"Interview Round {i} Input:\n{input_file.read_text()}\n"
                )
            if response_file.exists():
                interview_history.append(
                    f"Interview Round {i} Response:\n{response_file.read_text()}\n"
                )
        except Exception as e:
            click.echo(f"Warning: Error reading interview round {i}: {str(e)}")

    return render_template(
        "interview.j2",
        topic=topic,
        perspective=perspective,
        round_num=round_num,
        user_input=user_input,
        history=history,
        interview_history=interview_history,
    )


def handle_interview_command(
    perspective: Optional[int] = None, continue_to_next_round: bool = False
) -> None:
    """Main handler for the interview command"""
    topic = Topic.load()
    if not topic:
        raise click.ClickException("No topic selected. Use 'cons init' to create one.")

    if not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    if continue_to_next_round:
        perspective_index = get_most_recent_perspective(topic)
        perspective = perspective_index

    # Use provided perspective index or prompt for selection
    perspective_index = (
        perspective if perspective is not None else select_perspective(topic)
    )
    if continue_to_next_round:
        current_round = topic.get_latest_interview_round(perspective_index) + 1
    else:
        current_round = 1

    click.echo(f"\nInterviewing perspective #{perspective_index}")

    # Create template content
    template = ["# Interview Questions\n\n"]
    if current_round > 1:
        prev_response_file = topic.interview_response_file(
            perspective_index, current_round - 1
        )
        if prev_response_file.exists():
            response = prev_response_file.read_text()
            template.append("Previous Response:\n")
            template.append("\n".join(f"> {line}" for line in response.splitlines()))
            template.append("\n\n---\n\n")
    template.append(
        "Please provide your questions or discussion points for this interview.\n"
    )

    perspective_data = get_perspective(topic, perspective_index)
    execute(
        topic=topic,
        user_input_filepath=topic.interview_input_file(
            perspective_index, current_round
        ),
        user_input_template="".join(template),
        build_prompt_fn=lambda t, i: _build_interview_prompt(
            t, perspective_data, perspective_index, current_round, i
        ),
        response_definition=Discussion,
        response_filepath=topic.interview_response_file(
            perspective_index, current_round
        ),
        display_fn=display_interview,
    )


@interview.command()
@click.option(
    "--perspective", "-p", type=int, help="Index of the perspective to interview"
)
def start(perspective: Optional[int]):
    """Start a new interview with a selected perspective"""
    handle_interview_command(perspective=perspective)


@interview.command()
def next():
    """Continue interview with the most recent perspective"""
    handle_interview_command(continue_to_next_round=True)
