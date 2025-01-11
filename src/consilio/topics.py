import click
import subprocess
from .models import Topic

def handle_topics_command() -> None:
    """Open the README.md file in the default editor"""
    topic = Topic.load()
    
    if not topic:
        click.echo("No README.md found in current directory.")
        return
        
    editor = click.get_editor()
    try:
        click.edit(filename="README.md")
    except subprocess.SubprocessError:
        click.echo("Failed to open README.md in editor")
