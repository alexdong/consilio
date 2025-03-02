import click
import json
from pathlib import Path

from consilio.models import Topic, Perspective, display_perspectives
from consilio.utils import render_template
from consilio.executor import execute


@click.group()
def perspectives():
    pass


@perspectives.command()
def generate():
    """Generate perspectives for a topic using LLM"""
    topic = Topic.load()
    num = click.prompt(
        "How many perspectives would you like? (1-10)",
        type=click.IntRange(1, 10),
        default=5,
    )

    execute(
        topic=topic,
        user_input_filepath=None,
        user_input_template="",
        build_prompt_fn=lambda t, _: render_template(
            "perspectives.j2",
            topic=t,
            num_of_perspectives=num,
        ),
        response_definition=list[Perspective],
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

    # Get existing perspectives
    existing_items: list[Perspective] = []
    if topic.perspectives_file.exists():
        existing_items = json.loads(topic.perspectives_file.read_text())

    def save_and_append(new_perspective: Perspective, file: Path) -> None:
        """Custom save function that appends to existing perspectives"""
        perspectives = existing_items + [new_perspective.model_dump()]
        json_str = json.dumps(perspectives, indent=2)
        file.write_text(json_str)

    new_perspective = execute(
        topic=topic,
        user_input_filepath=None,
        user_input_template="",
        build_prompt_fn=lambda t, _: render_template(
            "additional_perspective.j2",
            topic=t,
            description=description,
            existing_perspectives=existing_items,
        ),
        response_definition=Perspective,
        response_filepath=topic.perspectives_file,
        display_fn=lambda p: display_perspectives([p] + existing_items),
    )

    # Save the new perspective
    save_and_append(Perspective(**new_perspective), topic.perspectives_file)


if __name__ == "__main__":
    generate()
