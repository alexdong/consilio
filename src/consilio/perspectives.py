import logging
import click
import json
import jsonschema
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from consilio.models import Topic
from consilio.utils import get_llm_response, render_template

schema = (Path(__file__).parent / "schemas" / "perspectives_schema.json").read_text()

def display_perspectives(perspectives: list) -> None:
    """Display perspectives in markdown format using rich"""
    console = Console()
    
    # Build markdown content
    md_content = "# Generated Perspectives\n\n"
    for i, perspective in enumerate(perspectives, 1):
        md_content += f"## {i}. {perspective.get('name', 'Unnamed Perspective')}\n\n"
        if 'expertise' in perspective:
            md_content += f"* **Expertise:** {perspective['expertise']}\n"
        if 'goal' in perspective:
            md_content += f"* **Goal:** {perspective['goal']}\n"
        if 'role' in perspective:
            md_content += f"* **Role:** {perspective['role']}\n"
        md_content += "\n"
    
    # Display using rich
    console.print(Markdown(md_content))


def validate_perspectives(perspectives: list) -> None:
    """Validate perspectives against schema"""
    jsonschema.validate(instance=perspectives, schema=json.loads(schema))


def generate_perspectives(topic: Topic) -> None:
    """Generate perspectives for a topic using LLM"""
    logger = logging.getLogger("consilio.perspectives")
    logger.info("Generating new perspectives")
    # Prompt for number of perspectives
    num = click.prompt(
        "How many perspectives would you like? (1-10)",
        type=click.IntRange(1, 10),
        default=5,
    )

    prompt = render_template(
        "perspectives.j2",
        topic=topic,
        num_of_perspectives=num,
        schema=schema,
    )
    system_prompt = render_template("system.j2")

    try:
        perspectives = get_llm_response(prompt, system_prompt=system_prompt)

        # Validate perspectives against schema
        validate_perspectives(perspectives)  # type: ignore

        # Save perspectives to file
        json_str = json.dumps(perspectives, indent=2)
        topic.perspectives_file.write_text(json_str)
        click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")
        
        # Display perspectives in markdown format
        display_perspectives(perspectives)
        
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
