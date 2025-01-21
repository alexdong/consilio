import logging
import click
import json
from rich.console import Console
from rich.markdown import Markdown
from consilio.models import Topic, Perspective
from consilio.utils import get_llm_response, render_template

@click.group()
def perspectives():
    """Manage discussion perspectives"""
    pass

@perspectives.command()
def generate():
    """Generate a new set of perspectives"""
    handle_perspectives_command(generate=True)

@perspectives.command()
def add():
    """Add a single new perspective"""
    handle_perspectives_command(add=True)

@perspectives.command()
def edit():
    """Edit existing perspectives"""
    handle_perspectives_command(edit=True)


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

    perspectives = get_llm_response(prompt, response_definition=None)

    # Save perspectives to file
    perspectives_objects = [Perspective.model_validate(p) for p in perspectives]
    json_str = json.dumps([p.model_dump() for p in perspectives_objects], indent=2)
    topic.perspectives_file.write_text(json_str)
    click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")

    # Display perspectives in markdown format
    display_perspectives(perspectives)  # type: ignore

    # Ask if user wants to edit
    if click.confirm("Would you like to edit the perspectives?"):
        click.echo("Opening perspectives file in editor...")
        click.edit(filename=str(topic.perspectives_file))


def add_perspective(topic: Topic) -> None:
    """Add a new perspective by prompting user for role and generating details"""
    logger = logging.getLogger("consilio.perspectives")
    logger.info("Adding new perspective")
    
    # Prompt for the role title
    description = click.prompt("Enter a description of the new perspective", type=str)
    
    # Generate details for this role using LLM
    # Load existing perspectives for context
    existing_perspectives = []
    if topic.perspectives_file.exists():
        existing_perspectives = json.loads(topic.perspectives_file.read_text())
    
    prompt = render_template(
        "additional_perspective.j2",
        topic=topic,
        description=description,
        existing_perspectives=existing_perspectives
    )
    new_perspective = get_llm_response(prompt, response_definition=None)
    if "perspectives" in new_perspective:
        # Handle case where LLM returns a dict with "perspectives" key
        new_perspective = new_perspective["perspectives"][0]
    existing_perspectives.append(new_perspective)
    
    # Save updated perspectives
    json_str = json.dumps(existing_perspectives, indent=2)
    topic.perspectives_file.write_text(json_str)
    
    click.echo(f"Added new perspective to: {topic.perspectives_file}")
    
    # Display the updated perspectives
    display_perspectives(existing_perspectives)

def edit_perspectives(topic: Topic) -> None:
    """Open perspectives file in editor"""
    logger = logging.getLogger("consilio.perspectives")
    logger.info("Opening perspectives file for editing")
    
    if not topic.perspectives_file.exists():
        click.echo("No perspectives file exists yet. Generate perspectives first.")
        return
        
    click.echo("Opening perspectives file in editor...")
    click.edit(filename=str(topic.perspectives_file))
    
    # Validate the file after editing
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        display_perspectives(perspectives)
    except json.JSONDecodeError:
        click.echo("Warning: The file contains invalid JSON. Please check the format.")

def handle_perspectives_command(generate: bool = True, add: bool = False, edit: bool = False) -> None:
    """Main handler for the perspectives command"""
    topic = Topic.load()
    if generate:
        generate_perspectives(topic)
    elif add:
        add_perspective(topic)
    elif edit:
        edit_perspectives(topic)
    else:
        # Default to generate if no subcommand specified
        generate_perspectives(topic)
