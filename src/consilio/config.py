import click
from pathlib import Path
from consilio.models import Config


def initialize_project(path: str) -> None:
    """Initialize a new Consilio project in the specified directory"""
    project_dir = Path(path).resolve()

    config_path = project_dir / "cons.toml"
    if config_path.exists():
        click.echo(f"Config file already exists at: {config_path}")
        return

    config = Config(config_path)
    config._save()
    click.echo(f"Initialized a new Consilio project in: {project_dir}")


def handle_init_command(path: str) -> None:
    """Main handler for the init command"""
    initialize_project(path)
