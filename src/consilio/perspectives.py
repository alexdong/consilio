import click
import json
import subprocess
from pathlib import Path
from typing import Optional
from .models import Config, Topic
from .utils import get_llm_response


def generate_perspectives(topic: Topic) -> None:
    """Generate perspectives for a topic using LLM"""
    prompt = f"""
    Please give me up to 5 distinct perspectives to discuss the following topic. 
    <Topic>
    {topic.description}
    </Topic>

    For each perspective, give me brief description of the following:

    Title: The name of the agent.
    Expertise: The scientific expertise the agent has.
    Goal: The ultimate goal of the agent in the context of the research project.
    Role: The specific role that the agent will play in the research project.

    Please make sure the response is in json.
    """

    try:
        perspectives = get_llm_response(prompt)

        # Save perspectives to file
        topic.perspectives_file.write_text(json.dumps(perspectives, indent=2))
        click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")

    except Exception as e:
        click.echo(f"Error generating perspectives: {str(e)}")


def edit_perspectives(topic: Topic) -> None:
    """Open perspectives file in editor"""
    if not topic.perspectives_file.exists():
        click.echo("No perspectives file exists yet. Generate perspectives first.")
        return

    try:
        subprocess.run(["open", "-t", str(topic.perspectives_file)])
    except subprocess.SubProcessError:
        click.echo("Failed to open perspectives file in editor")


def list_perspectives(topic: Topic) -> None:
    """List all perspectives with their details"""
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        click.echo("\nAvailable perspectives:")
        for i, perspective in enumerate(perspectives):
            click.echo(f"\n{i}. {perspective.get('Title', 'Unnamed')}")
            click.echo(f"   Expertise: {perspective.get('Expertise', 'N/A')}")
            click.echo(f"   Goal: {perspective.get('Goal', 'N/A')}")
            click.echo(f"   Role: {perspective.get('Role', 'N/A')}")
    except (json.JSONDecodeError, FileNotFoundError):
        click.echo("No valid perspectives found. Generate perspectives first.")


def handle_perspectives_command(edit: bool, list_flag: bool) -> None:
    """Main handler for the perspectives command"""
    config = Config()
    topic = config.current_topic

    if not topic:
        click.echo(
            "No topic currently selected. Use 'cons topics -t <number>' to select one."
        )
        return

    if list_flag:
        list_perspectives(topic)
    elif edit:
        edit_perspectives(topic)
    else:
        generate_perspectives(topic)
