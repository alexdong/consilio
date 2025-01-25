import logging
import click
import json
from pathlib import Path
from typing import List
from consilio.models import Topic, Perspective, display_perspectives
from consilio.utils import get_llm_response, render_template
from consilio.executor import execute

@click.group()
def perspectives():
    pass


@click.command()
def generate():
    """Generate perspectives for a topic using LLM"""
    topic = Topic.load()
    num = click.prompt(
        "How many perspectives would you like? (1-25)",
        type=click.IntRange(1, 25),
        default=10,
    )

    execute(
        topic=topic,
        build_prompt_fn=lambda t, _: render_template(
            "perspectives.j2",
            topic=t,
            num_of_perspectives=num,
        ),
        response_definition=List[Perspective],
        response_filepath=topic.perspectives_file,
        display_fn=display_perspectives,
    )

    # Ask if user wants to edit
    if click.confirm("Would you like to edit the perspectives?"):
        click.echo("Opening perspectives file in editor...")
        click.edit(filename=str(topic.perspectives_file))


@perspectives.command()
def add():
    """Add a new perspective by prompting user for role and generating details"""
    topic = Topic.load()
    description = click.prompt("Enter a description of the new perspective", type=str)
    
    existing_perspectives = []
    if topic.perspectives_file.exists():
        existing_perspectives = json.loads(topic.perspectives_file.read_text())
    
    def save_and_append(new_perspective: Perspective, file: Path) -> None:
        """Custom save function that appends to existing perspectives"""
        existing_perspectives.append(new_perspective.model_dump())
        json_str = json.dumps(existing_perspectives, indent=2)
        file.write_text(json_str)
    
    execute(
        topic=topic,
        build_prompt_fn=lambda t, _: render_template(
            "additional_perspective.j2",
            topic=t,
            description=description,
            existing_perspectives=existing_perspectives
        ),
        response_definition=Perspective,
        response_filepath=topic.perspectives_file,
        display_fn=lambda p: display_perspectives([p] + existing_perspectives),
        save_fn=save_and_append
    )

