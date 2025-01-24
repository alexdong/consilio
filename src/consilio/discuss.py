import click
import json
import logging
from typing import Optional, List, Dict
from rich.console import Console
from rich.markdown import Markdown
from consilio.models import Topic, Discussion
from consilio.utils import get_llm_response, render_template


def display_discussion(discussion_list: List[Dict[str, str]]) -> None:
    """Display discussion in markdown format using rich"""
    console = Console()

    # Convert to Discussion objects if they're dicts
    discussions = [Discussion.from_dict(d) for d in discussion_list]

    # Build markdown content from Discussion objects
    md_content = "## Discussion Round\n\n" + "".join(
        d.to_markdown() for d in discussions
    )

    # Display using rich
    console.print(Markdown(md_content))


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


def start_discussion_round(
    topic: Topic, round_num: int, user_input: Optional[str]
) -> None:
    """Start a new discussion round"""
    logger = logging.getLogger("consilio.discuss")
    logger.info(f"Starting discussion round {round_num}")
    # Build appropriate prompt based on round number
    if round_num == 1:
        prompt = _build_first_round_prompt(topic)
    else:
        prompt = _build_subsequent_round_prompt(topic, round_num, user_input=user_input)

    # Get LLM response with system prompt
    response = get_llm_response(prompt)

    # Display the discussion
    display_discussion(response)  # type: ignore

    discussion_objects = [Discussion.model_validate(d) for d in response]
    json_str = json.dumps([p.model_dump() for p in discussion_objects], indent=2)
    discussion_output_file = topic.discussion_response_file(round_num)
    discussion_output_file.write_text(json_str)
    click.echo(f"Generated discussion response to: {discussion_output_file}")



@click.command()    
def discuss():
    """Main handler for the discuss command"""
    topic = Topic.load()

    # Determine round number
    current_round = round if round else topic.latest_discussion_round + 1
    if current_round == 1 and not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    # Get user input for the round
    user_input = []
    if current_round > 1 and click.confirm(
        "\nWould you like to provide your input?", default=True
    ):
        # Create input file if it doesn't exist
        input_file = topic.discussion_input_file(current_round)
        if not input_file.exists():
            # Include previous round's response if available
            if current_round > 1:
                prev_response_file = topic.discussion_response_file(current_round - 1)
                prev_discussions = json.loads(prev_response_file.read_text())

                for d in prev_discussions:
                    discussion = Discussion.model_validate(d)
                    user_input.extend(f"> {line}" for line in discussion.to_markdown().splitlines())
            else:
                user_input.extend([
                    "Please provide guidance for the discussion.",
                    "- Answer questions from the previous round of discussions",
                    "- Specify particular areas you'd like to focus on next",
                ])
            
            user_input = click.edit(text="\n".join(user_input))
            input_file.write_text(user_input)
        else:
            user_input = input_file.read_text()

    click.echo(f"\nStarting discussions (Round #{current_round}) ...")
    start_discussion_round(topic, current_round, user_input)
