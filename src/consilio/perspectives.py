import logging
import click
import json
import jsonschema
from typing import List
from rich.console import Console
from rich.markdown import Markdown
from consilio.models import Topic, Perspective
from consilio.utils import get_llm_response, render_template


def display_perspectives(perspectives: list) -> None:
    """Display perspectives in markdown format using rich"""
    console = Console()

    # Convert perspectives to Perspective objects if they're dicts
    perspectives = [Perspective.model_validate(p) for p in perspectives]

    # Build markdown content from Perspective objects
    md_content = "".join(p.to_markdown(i) for i, p in enumerate(perspectives, 1))

    # Display using rich
    console.print(Markdown(md_content))


def generate_perspectives(topic: Topic) -> None:
    """Generate perspectives for a topic using LLM"""
    logger = logging.getLogger("consilio.perspectives")
    logger.info("Generating new perspectives")
    # Prompt for number of perspectives
    num = click.prompt(
        "How many perspectives would you like? It's often beneficial to start with a larger number of persepctives before trimming the number down. (1-25)",
        type=click.IntRange(1, 25),
        default=10,
    )

    prompt = render_template(
        "perspectives.j2",
        topic=topic,
        num_of_perspectives=num,
    )

    try:
        perspectives = get_llm_response(prompt, response_definition=List[Perspective])

        # Save perspectives to file
        perspectives_objects = [Perspective.model_validate(p) for p in perspectives]
        json_str = json.dumps([p.to_json() for p in perspectives_objects], indent=2)
        topic.perspectives_file.write_text(json_str)
        click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")

        # Display perspectives in markdown format
        display_perspectives(perspectives)  # type: ignore

        # Ask if user wants to edit
        if click.confirm("Would you like to edit the perspectives?"):
            click.echo("Opening perspectives file in editor...")
            click.edit(filename=str(topic.perspectives_file))

    except jsonschema.ValidationError as e:
        click.echo(f"Generated perspectives failed validation: {str(e)}")
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON response from LLM: {str(e)}")
    except Exception as e:
        click.echo(f"Error generating perspectives: {str(e)}")


def handle_perspectives_command() -> None:
    """Main handler for the perspectives command"""
    topic = Topic.load()
    generate_perspectives(topic)
