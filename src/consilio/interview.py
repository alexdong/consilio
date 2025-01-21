import click
import json
import logging
from typing import Optional, Dict, Any
from consilio.models import Topic, Discussion
from consilio.utils import get_llm_response, render_template


def _get_perspective(topic: Topic, index: int) -> Dict[Any, Any]:
    """Get a specific perspective by index"""
    logger = logging.getLogger("consilio.interview")
    logger.debug(f"Getting perspective {index}")
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        if index < 0 or index >= len(perspectives):
            raise click.ClickException(
                f"Invalid perspective index. Must be between 0 and {len(perspectives)-1}"
            )
        return perspectives[index]
    except (json.JSONDecodeError, FileNotFoundError):
        raise click.ClickException(
            "No valid perspectives found. Generate perspectives first."
        )


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
    for i in range(1, round_num):
        try:
            input_file = topic.interview_input_file(perspective_index, i)
            response_file = topic.interview_response_file(perspective_index, i)

            if input_file.exists():
                history.append(
                    f"Interview Round {i} Input:\n{input_file.read_text()}\n"
                )
            if response_file.exists():
                history.append(
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
    )


def start_interview_round(
    topic: Topic, perspective_index: int, round_num: int, user_input: str
) -> None:
    """Start a new interview round with a specific perspective"""
    logger = logging.getLogger("consilio.interview")
    logger.info(
        f"Starting interview round {round_num} with perspective {perspective_index}"
    )
    logger.debug(f"Interview prompt length: {len(user_input)} chars")
    perspective = _get_perspective(topic, perspective_index)
    prompt = _build_interview_prompt(
        topic, perspective, perspective_index, round_num, user_input
    )

    # Save user input
    topic.interview_input_file(perspective_index, round_num).write_text(user_input)

    try:
        # Get LLM response
        response = Discussion.model_validate(
            get_llm_response(prompt, response_definition=Discussion)
        )

        # Save response
        topic.interview_response_file(perspective_index, round_num).write_text(
            response.model_dump_json(indent=2)
        )

        click.echo(f"\nInterview round {round_num} completed.")
        click.echo(f"Files saved in: {topic.directory}")

    except Exception as e:
        raise click.ClickException(f"Error in interview round: {str(e)}")


def _select_perspective(topic: Topic) -> int:
    """Display perspective selection menu and get user choice"""
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        click.echo("\nAvailable perspectives:")
        for idx, p in enumerate(perspectives):
            click.echo(f"\n{idx}. {p.get('title', 'Untitled')}")
            click.echo(f"   Expertise: {p.get('expertise', 'N/A')}")
        
        while True:
            try:
                choice = click.prompt("\nSelect perspective number", type=int)
                if 0 <= choice < len(perspectives):
                    return choice
                click.echo("Invalid selection. Please try again.")
            except click.Abort:
                raise click.ClickException("Selection aborted")
    except (json.JSONDecodeError, FileNotFoundError):
        raise click.ClickException("No valid perspectives found. Generate perspectives first.")

def _get_most_recent_perspective(topic: Topic) -> Optional[int]:
    """Find the most recently interviewed perspective"""
    latest_perspective = None
    latest_round = -1
    
    # Check all potential perspective files
    for p_idx in range(100):  # reasonable upper limit
        round_num = topic.get_latest_interview_round(p_idx)
        if round_num > latest_round:
            latest_round = round_num
            latest_perspective = p_idx
    
    return latest_perspective

def handle_interview_command(mode: str = "start") -> None:
    """Main handler for the interview command"""
    topic = Topic.load()
    if not topic:
        raise click.ClickException("No topic selected. Use 'cons init' to create one.")

    if not topic.perspectives_file.exists():
        raise click.ClickException("No perspectives found. Generate perspectives first with 'cons perspectives'")

    # Get perspective index based on mode
    perspective_index = None
    if mode == "continue":
        perspective_index = _get_most_recent_perspective(topic)
        if perspective_index is None:
            click.echo("No previous interviews found.")
            return
    else:  # start mode
        perspective_index = _select_perspective(topic)

    # Determine round number
    current_round = topic.get_latest_interview_round(perspective_index) + 1

    # Get user input for the round
    click.echo(f"\nInterviewing perspective #{perspective_index}")
    click.echo("Please provide your questions or discussion points.")
    click.echo("Press Ctrl+D when finished.\n")

    user_input = click.get_text_stream("stdin").read().strip()
    if not user_input:
        raise click.ClickException("No input provided")

    click.echo(f"\nStarting interview (Round #{current_round}) ...")
    start_interview_round(topic, perspective_index, current_round, user_input)
