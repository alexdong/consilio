import click
import subprocess
from pathlib import Path
from .models import Config

def handle_topics_command() -> None:
    """Open the discussion.md file in the default editor"""
    config = Config()
    topic = config.current_topic
    
    if not topic:
        click.echo("No topic currently selected.")
        return
        
    editor = click.get_editor()
    try:
        click.edit(filename=str(topic.discussion_file))
    except subprocess.SubprocessError:
        click.echo("Failed to open discussion file in editor")
