import click
import json
import logging
from typing import Optional, List
from consilio.models import Topic, Discussion, display_discussions
from consilio.utils import render_template
from consilio.executor import execute



def _build_first_round_prompt(topic: Topic) -> str:
    """Build prompt for the first discussion round"""
    logger = logging.getLogger("consilio.discuss")
    logger.debug("Building first round prompt")

    return render_template(
        "first_round.j2", topic=topic, perspectives=topic.perspectives
    )


def _build_subsequent_round_prompt(
    topic: Topic, round_num: int, user_input: Optional[str]
) -> str:
    """Build prompt including previous rounds' context"""
    logger = logging.getLogger("consilio.discuss")
    logger.debug(f"Building prompt for round {round_num}")
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
            click.echo(f"Warning: Error reading round {i}: {str(e)}")

    context = "\n".join(history)
    return render_template(
        "subsequent_round.j2",
        context=context,
        topic=topic,
        round_num=round_num,
        user_input=user_input,
    )


@click.command()    
def discuss():
    """Main handler for the discuss command"""
    topic = Topic.load()
    current_round = topic.latest_discussion_round + 1

    if current_round == 1 and not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    # Prepare input_template for user input
    input_template = []
    if current_round > 1:
        prev_response_file = topic.discussion_response_file(current_round - 1)
        prev_discussions = json.loads(prev_response_file.read_text())
        for d in prev_discussions:
            discussion = Discussion.model_validate(d)
            input_template.extend(f"> {line}" for line in discussion.to_markdown().splitlines())
    else:
        input_template.extend([
            "Please provide guidance for the discussion.",
            "- Answer questions from the previous round of discussions",
            "- Specify particular areas you'd like to focus on next",
        ])

    # Build prompt based on round
    def build_prompt(topic: Topic, user_input: str = "") -> str:
        if current_round == 1:
            return _build_first_round_prompt(topic)
        else:
            return _build_subsequent_round_prompt(topic, round_num=current_round, user_input=user_input)

    if current_round == 1:
        user_input_filepath = None
    else:
        user_input_filepath = topic.discussion_input_file(current_round)

    execute(
        topic=topic,
        user_input_filepath=user_input_filepath,
        user_input_template="\n".join(input_template),
        build_prompt_fn=build_prompt, 
        response_definition=List[Discussion],
        response_filepath=topic.discussion_response_file(current_round),
        display_fn=display_discussions,
    )

