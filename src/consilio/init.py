import subprocess

import click
import tomli_w

from consilio.models import Topic
from consilio.utils import render_template


@click.command()
def init() -> None:
    """Initialize a new project and open README.md in editor"""
    topic = Topic.load()
    readme_path = topic.discussion_file
    config_path = topic.config_file

    # Create cons.toml if it doesn't exist
    if not config_path.exists():
        config = {
            "key_bindings": "emacs",
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 1.0,
        }
        config_path.write_text(tomli_w.dumps(config))
        click.echo(f"Created cons.toml in: {config_path}")

    # Create/edit README.md
    if not readme_path.exists():
        content = render_template("README.j2")
        readme_path.write_text(content)
        click.echo(f"Created README.md in: {readme_path}")
    else:
        content = readme_path.read_text()

    try:
        # click.edit with filename doesn't take text parameter
        click.edit(filename=str(readme_path))
    except subprocess.SubprocessError:
        click.echo(f"Failed to open {readme_path} in editor")
