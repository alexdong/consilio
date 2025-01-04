import click
import json
import subprocess
from typing import Optional, List, Dict
from dataclasses import dataclass
from .models import Topic, Config
from .utils import get_llm_response, render_template


def list_topics() -> None:
    """List all available topics with numbers"""
    topics = Topic.list_all()
    if not topics:
        click.echo("No topics found.")
        return

    click.echo("\nAvailable topics:")
    for i, topic in enumerate(topics, 1):
        first_line = topic.description.split("\n")[0]
        click.echo(f"{i}. [{topic.created_at:%Y-%m-%d}] {first_line}")


def switch_topic(topic_number: int) -> None:
    """Switch to a different topic by number"""
    topics = Topic.list_all()
    if not topics:
        click.echo("No topics found.")
        return

    if topic_number < 1 or topic_number > len(topics):
        click.echo(f"Invalid topic number. Please choose between 1 and {len(topics)}")
        return

    config = Config()
    config.current_topic = topics[topic_number - 1]
    click.echo(f"Switched to topic: {topics[topic_number - 1].slug}")


def open_topic_directory() -> None:
    """Open current topic directory in system file explorer"""
    config = Config()
    topic = config.current_topic

    if not topic:
        click.echo("No topic currently selected.")
        return

    # Use 'open' command on macOS
    try:
        subprocess.run(["open", str(topic.directory)])
    except subprocess.SubprocessError:
        click.echo("Failed to open directory in file explorer")


@dataclass
class Round:
    number: int
    input: str
    response: str


def generate_summary(topic: Topic) -> None:
    """Generate a summary of all discussion rounds"""
    if not topic.discussion_file.exists():
        click.echo("No discussion file found.")
        return

    rounds: List[Round] = []
    
    # Gather all rounds
    current_round = 1
    while True:
        input_file = topic.round_input_file(current_round)
        response_file = topic.round_response_file(current_round)
        
        if not input_file.exists() or not response_file.exists():
            break
            
        rounds.append(Round(
            number=current_round,
            input=input_file.read_text(),
            response=response_file.read_text()
        ))
        current_round += 1

    if not rounds:
        click.echo("No discussion rounds found.")
        return

    # Generate summary using template
    prompt = render_template("summary.j2", topic=topic, rounds=rounds)
    system_prompt = render_template("system.j2")

    try:
        summary = get_llm_response(prompt, system_prompt=system_prompt)
        
        # Save summary
        summary_file = topic.directory / "summary.md"
        summary_file.write_text(summary)
        click.echo(f"Summary generated and saved to: {summary_file}")
        
    except Exception as e:
        click.echo(f"Error generating summary: {str(e)}")


def handle_topics_command(
    list_flag: bool, topic_number: Optional[int], open_flag: bool, summary: bool = False
) -> None:
    """Main handler for the topics command"""
    if summary:
        config = Config()
        topic = config.current_topic
        if not topic:
            click.echo("No topic currently selected. Use 'cons topics -t <number>' to select one.")
            return
        generate_summary(topic)
    elif list_flag:
        list_topics()
    elif topic_number is not None:
        switch_topic(topic_number)
    elif open_flag:
        open_topic_directory()
    else:
        # Default behavior: list topics
        list_topics()
