import json
import logging

import click

from consilio.executor import execute
from consilio.models import Discussion, Topic, display_discussions
from consilio.utils import render_template


def _build_first_round_prompt(topic: Topic) -> str:
    """Build prompt for the first discussion round"""
    logger = logging.getLogger("consilio.discuss")
    logger.debug("Building first round prompt")

    return render_template(
        "first_round.j2",
        topic=topic,
        perspectives=topic.perspectives,
    )


def _build_subsequent_round_prompt(
    topic: Topic,
    round_num: int,
    user_input: str | None,
) -> str:
    """Build prompt including previous rounds' context"""
    logger = logging.getLogger("consilio.discuss")
    logger.debug("Building prompt for round %s", round_num)
    history = []

    # Gather all previous rounds
    for i in range(1, round_num):
        try:
            input_file = topic.discussion_input_file(i)
            response_file = topic.discussion_response_file(i)

            history.append(f"<Discussion round='{i}'>")
            if input_file.exists():
                history.append(f"<input>{input_file.read_text()}</input>\n")
            if response_file.exists():
                history.append(f"<response>\n{response_file.read_text()}</response>\n")
            history.append("</Discussion>\n")
        except Exception as e:
            click.echo(f"Warning: Error reading round {i}: {e!s}")

    context = "\n".join(history)
    return render_template(
        "subsequent_round.j2",
        context=context,
        topic=topic,
        round_num=round_num,
        user_input=user_input,
    )


def _prepare_input_template(topic: Topic, current_round: int) -> list[str]:
    """Prepare input template for user guidance"""
    if current_round == 1:
        return [
            "Please provide guidance for the discussion.",
            "- Answer questions from the previous round of discussions",
            "- Specify particular areas you'd like to focus on next",
        ]

    # Load previous discussions for subsequent rounds
    input_template: list[str] = []
    prev_response_file = topic.discussion_response_file(current_round - 1)
    prev_discussions = json.loads(prev_response_file.read_text())

    for d in prev_discussions:
        discussion = Discussion.model_validate(d)
        input_template.extend(
            f"> {line}" for line in discussion.to_markdown().splitlines()
        )

    return input_template


@click.command()
@click.option(
    "--round",
    "round_num",
    type=int,
    help="Round number to re-run (defaults to next round)",
)
def discuss(round_num: int | None = None) -> None:
    """Main handler for the discuss command"""
    topic = Topic.load()
    current_round = (
        round_num if round_num is not None else topic.latest_discussion_round + 1
    )

    if current_round == 1 and not topic.perspectives_file.exists():
        msg = "No perspectives found. Generate perspectives first with 'cons perspectives'"
        raise click.ClickException(
            msg,
        )

    # Prepare input_template for user input
    input_template = _prepare_input_template(topic, current_round)

    # Build prompt based on round
    def build_prompt(topic: Topic, user_input: str = "") -> str:
        if current_round == 1:
            return _build_first_round_prompt(topic)
        return _build_subsequent_round_prompt(
            topic,
            round_num=current_round,
            user_input=user_input,
        )

    user_input_filepath = (
        None if current_round == 1 else topic.discussion_input_file(current_round)
    )

    execute(
        topic=topic,
        user_input_filepath=user_input_filepath,
        user_input_template="\n".join(input_template),
        build_prompt_fn=build_prompt,
        response_definition=None,
        response_filepath=topic.discussion_response_file(current_round),
        display_fn=display_discussions,
    )
