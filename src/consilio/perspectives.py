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
    For each perspective, give me brief description of the following:

    Title: The name of the agent.
    Expertise: The scientific expertise the agent has.
    Goal: The ultimate goal of the agent in the context of the research project.
    Role: The specific role that the agent will play in the research project.

    Topic: {topic.description}

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
        subprocess.run(['open', '-t', str(topic.perspectives_file)])
    except subprocess.SubProcessError:
        click.echo("Failed to open perspectives file in editor")

def handle_perspectives_command(edit: bool) -> None:
    """Main handler for the perspectives command"""
    config = Config()
    topic = config.current_topic
    
    if not topic:
        click.echo("No topic currently selected. Use 'cons topics -t <number>' to select one.")
        return
        
    if edit:
        edit_perspectives(topic)
    else:
        generate_perspectives(topic)