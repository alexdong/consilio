import click
import subprocess
from consilio.models import Config


def create_or_edit_config() -> None:
    """Create config file if it doesn't exist and open it in editor"""
    config = Config()

    # Ensure config file exists with defaults
    if not config.path.exists():
        click.echo("Creating new config file with defaults...")
        config._save()

    # Open in default editor
    try:
        click.echo(f"Opening config file: {config.path}")
        subprocess.run(["open", "-t", str(config.path)])
    except subprocess.SubProcessError:
        click.echo("Failed to open config file in editor")


def handle_config_command() -> None:
    """Main handler for the config command"""
    create_or_edit_config()
