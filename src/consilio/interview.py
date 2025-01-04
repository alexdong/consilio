import click
import json
from typing import Optional, Dict, Any
from consilio.models import Config, Topic
from consilio.utils import get_llm_response, render_template


def _get_perspective(topic: Topic, index: int) -> Dict[Any, Any]:
    """Get a specific perspective by index"""
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
    topic: Topic, perspective: Dict[Any, Any], perspective_index: int, round_num: int, user_input: str
) -> str:
    """Build prompt for interview rounds"""
    history = []

    # Add context from discussion rounds
    for i in range(1, topic.latest_round + 1):
        try:
            input_file = topic.round_input_file(i)
            response_file = topic.round_response_file(i)

            if input_file.exists():
                history.append(f"Discussion Round {i} Input:\n{input_file.read_text()}\n")
            if response_file.exists():
                history.append(f"Discussion Round {i} Response:\n{response_file.read_text()}\n")
        except Exception as e:
            click.echo(f"Warning: Error reading discussion round {i}: {str(e)}")

    # Add context from previous interview rounds
    for i in range(1, round_num):
        try:
            input_file = topic.interview_input_file(perspective_index, i)
            response_file = topic.interview_response_file(perspective_index, i)

            if input_file.exists():
                history.append(f"Interview Round {i} Input:\n{input_file.read_text()}\n")
            if response_file.exists():
                history.append(f"Interview Round {i} Response:\n{response_file.read_text()}\n")
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
    perspective = _get_perspective(topic, perspective_index)
    prompt = _build_interview_prompt(topic, perspective, perspective_index, round_num, user_input)

    # Save user input
    topic.interview_input_file(perspective_index, round_num).write_text(user_input)

    try:
        # Get LLM response
        response = get_llm_response(prompt)

        # Save response
        topic.interview_response_file(perspective_index, round_num).write_text(
            json.dumps(response, indent=2)
        )

        click.echo(f"\nInterview round {round_num} completed.")
        click.echo(f"Files saved in: {topic.directory}")

    except Exception as e:
        raise click.ClickException(f"Error in interview round: {str(e)}")


def handle_interview_command(perspective_index: int, round: Optional[int]) -> None:
    """Main handler for the interview command"""
    config = Config()
    topic = config.current_topic

    if not topic:
        raise click.ClickException(
            "No topic selected. Use 'cons topics -t <number>' to select one."
        )

    if not topic.perspectives_file.exists():
        raise click.ClickException(
            "No perspectives found. Generate perspectives first with 'cons perspectives'"
        )

    # Determine round number
    current_round = round if round else topic.latest_interview_round + 1

    # Get user input for the round
    click.echo(f"\nInterviewing perspective #{perspective_index}")
    click.echo("Please provide your questions or discussion points.")
    click.echo("Press Ctrl+D when finished.\n")

    user_input = click.get_text_stream("stdin").read().strip()
    if not user_input:
        raise click.ClickException("No input provided")

    click.echo(f"\nStarting interview (Round #{current_round}) ...")
    start_interview_round(topic, perspective_index, current_round, user_input)
