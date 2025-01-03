import click
import subprocess
from typing import Optional
from .models import Topic, Config


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
    except subprocess.SubProcessError:
        click.echo("Failed to open directory in file explorer")


def handle_topics_command(
    list_flag: bool, topic_number: Optional[int], open_flag: bool
) -> None:
    """Main handler for the topics command"""
    if list_flag:
        list_topics()
    elif topic_number is not None:
        switch_topic(topic_number)
    elif open_flag:
        open_topic_directory()
    else:
        # Default behavior: list topics
        list_topics()
