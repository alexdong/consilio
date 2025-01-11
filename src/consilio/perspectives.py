import logging
import click
import json
import jsonschema
from pathlib import Path
from .models import Topic
from .utils import get_llm_response, render_template


def validate_perspectives(perspectives: list) -> None:
    """Validate perspectives against schema"""
    schema_path = Path(__file__).parent / "schemas" / "perspectives_schema.json"
    schema = json.loads(schema_path.read_text())
    jsonschema.validate(instance=perspectives, schema=schema)


def generate_perspectives(topic: Topic) -> None:
    """Generate perspectives for a topic using LLM"""
    logger = logging.getLogger("consilio.perspectives")
    logger.info("Generating new perspectives")
    # Prompt for number of perspectives
    num = click.prompt("How many perspectives would you like? (1-10)", 
                      type=click.IntRange(1, 10),
                      default=5)
    
    # Load schema for template
    schema_path = Path(__file__).parent / "schemas" / "perspectives_schema.json"
    schema = json.loads(schema_path.read_text())
    
    prompt = render_template("perspectives.j2", 
                           topic=topic,
                           num_of_perspectives=num,
                           schema=json.dumps(schema, indent=2))
    system_prompt = render_template("system.j2")

    try:
        perspectives = json.loads(get_llm_response(prompt, system_prompt=system_prompt))
        
        # Validate perspectives against schema
        validate_perspectives(perspectives)

        # Save perspectives to file
        topic.perspectives_file.write_text(json.dumps(perspectives, indent=2))
        click.echo(f"Generated perspectives saved to: {topic.perspectives_file}")

    except jsonschema.exceptions.ValidationError as e:
        click.echo(f"Generated perspectives failed validation: {str(e)}")
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON response from LLM: {str(e)}")
    except Exception as e:
        click.echo(f"Error generating perspectives: {str(e)}")


def handle_perspectives_command() -> None:
    """Main handler for the perspectives command"""
    topic = Topic.load()
    generate_perspectives(topic)
