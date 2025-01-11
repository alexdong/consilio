import click
import subprocess
from .models import Topic
from .utils import render_template


def handle_edit_command() -> None:
    """Open the README.md file in the default editor"""
    topic = Topic.load()
    if not topic.discussion_file.exists():
        content = render_template("edit.j2")
        topic.discussion_file.write_text(content)
    else:
        content = topic.discussion_file.read_text()

    try:
        click.edit(
            text=content,  # Prepopulate the editor with the file content
            filename="README.md",
        )
    except subprocess.SubprocessError:
        click.echo("Failed to open README.md in editor")
