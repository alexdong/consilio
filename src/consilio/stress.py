import json
import logging
import click
from typing import List
from dataclasses import dataclass
from .models import Topic
from .utils import get_llm_response, render_template

@dataclass
class Round:
    number: int
    input: str
    response: str

def get_stress_analysis(topic: Topic) -> None:
    """Generate stress analysis of current discussion"""
    logger = logging.getLogger("consilio.stress")
    logger.info("Generating stress analysis")
    
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

    # Generate analysis using template
    prompt = render_template("stress.j2", topic=topic, rounds=rounds)
    system_prompt = render_template("system.j2")

    try:
        analysis = get_llm_response(prompt, system_prompt=system_prompt)
        
        # Save analysis
        stress_file = topic.directory / "stress_analysis.json"
        stress_file.write_text(json.dumps(analysis, indent=2))
        click.echo(f"Stress analysis saved to: {stress_file}")
        
    except Exception as e:
        click.echo(f"Error generating stress analysis: {str(e)}")


def handle_stress_command() -> None:
    """Main handler for the stress command"""
    topic = Topic.load()
    if not topic:
        raise click.ClickException(
            "No topic selected. Use 'cons topics -t <number>' to select one."
        )

    get_stress_analysis(topic)
