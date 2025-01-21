import click
import json
import logging
from typing import Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from consilio.models import Topic, Discussion
from consilio.utils import get_llm_response, render_template
from consilio.perspective_utils import select_perspective, get_most_recent_perspective, get_perspective

def display_interview(discussion: Discussion) -> None:
    """Display interview response in markdown format"""
    console = Console()
    md_content = "## Interview Response\n\n" + discussion.to_markdown()
    console.print(Markdown(md_content))

def _build_interview_prompt(
    topic: Topic,
    perspective: Dict[Any, Any],
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

def start_interview_round(
    topic: Topic, perspective_index: int, round_num: int, user_input: str
) -> None:
    """Start a new interview round with a specific perspective"""
    logger = logging.getLogger("consilio.interview")
    logger.info(
        f"Starting interview round {round_num} with perspective {perspective_index}"
    )
    
    # Get perspective and build prompt
    perspective = get_perspective(topic, perspective_index)
    prompt = _build_interview_prompt(
        topic, perspective, perspective_index, round_num, user_input
    )

    # Save user input
    input_file = topic.interview_input_file(perspective_index, round_num)
    input_file.write_text(user_input)
    logger.debug(f"Saved interview input to {input_file}")

    try:
        # Get LLM response
        response = get_llm_response(prompt, response_definition=Discussion)
        discussion = Discussion.model_validate(response)
        
        # Display the response
        display_interview(discussion)

        # Save response
        response_file = topic.interview_response_file(perspective_index, round_num)
        response_file.write_text(discussion.model_dump_json(indent=2))
        logger.debug(f"Saved interview response to {response_file}")

    except Exception as e:
        logger.error(f"Error in interview round: {str(e)}")
        raise click.ClickException(f"Error in interview round: {str(e)}")

@click.group()
def interview():
    """Manage perspective interviews"""
    pass

@interview.command()
@click.option('--perspective', '-p', type=int, help='Index of the perspective to interview')
def start(perspective: Optional[int]):
    """Start a new interview with a selected perspective"""
    logger = logging.getLogger("consilio.interview")
    topic = Topic.load()
    if not topic:
        raise click.ClickException("No topic selected. Use 'cons init' to create one.")

    if not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    # Use provided perspective index or prompt for selection
    perspective_index = perspective if perspective is not None else select_perspective(topic)
    current_round = topic.get_latest_interview_round(perspective_index) + 1
    input_file = topic.interview_input_file(perspective_index, current_round)
    if input_file.exists() and click.confirm(f"Input file {input_file} already exists. Overwrite?", default=False):
        input_file.unlink()

    # Create template content
    template = ["# Interview Questions\n\n"]
    
    # If the input file already exists, it means that the user wants to re-send the same questions.
    if not input_file.exists():
        if current_round > 1:
            prev_response_file = topic.interview_response_file(perspective_index, current_round - 1)
            if prev_response_file.exists():
                try:
                    response = prev_response_file.read_text()
                    template.append("Previous Response:\n")
                    template.append(response)
                    template.append("\n---\n\n")
                except Exception as e:
                    logger.warning(f"Could not load previous response: {e}")
        
        template.append("Please provide your questions or discussion points for this interview.\n")
        input_file.write_text("".join(template))
    
    # Open editor for input
    user_input = click.edit(filename=str(input_file))
    if not user_input:
        raise click.ClickException("No input provided")

    click.echo(f"\nStarting interview (Round #{current_round}) ...")
    start_interview_round(topic, perspective_index, current_round, user_input)

@interview.command()
def continue_():
    """Continue interview with the most recent perspective"""
    topic = Topic.load()
    if not topic:
        raise click.ClickException("No topic selected. Use 'cons init' to create one.")

    if not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    perspective_index = get_most_recent_perspective(topic)
    if perspective_index is None:
        click.echo("No previous interviews found.")
        return

    current_round = topic.get_latest_interview_round(perspective_index) + 1

    click.echo(f"\nContinuing interview with perspective #{perspective_index}")
    click.echo("Please provide your questions or discussion points.")
    click.echo("Press Ctrl+D when finished.\n")

    user_input = click.get_text_stream("stdin").read().strip()
    if not user_input:
        raise click.ClickException("No input provided")

    click.echo(f"\nStarting interview (Round #{current_round}) ...")
    start_interview_round(topic, perspective_index, current_round, user_input)

# Set default command
interview.default_command = "start"
