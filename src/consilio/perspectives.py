import logging
import click
import json
import jsonschema
from pathlib import Path
from consilio.models import Topic
from consilio.utils import get_llm_response, render_template

schema = (Path(__file__).parent / "schemas" / "perspectives_schema.json").read_text()


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
        topic.perspectives_file.write_text(json.dumps(perspectives, indent=2))
        click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")

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
