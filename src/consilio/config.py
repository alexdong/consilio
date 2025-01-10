import click
from pathlib import Path
from consilio.models import Config


def initialize_project(path: str) -> None:
    """Initialize a new Consilio project in the specified directory"""
    project_dir = Path(path).resolve()
    
    if not project_dir.exists():
        project_dir.mkdir(parents=True)
        click.echo(f"Created directory: {project_dir}")

    config = Config(project_dir / "config.toml")
    
    if config.path.exists():
        click.echo(f"Config file already exists at: {config.path}")
        return

    click.echo(f"Initializing new Consilio project in: {project_dir}")
    config._save()
    click.echo(f"Created config file: {config.path}")


def handle_init_command(path: str) -> None:
    """Main handler for the init command"""
    initialize_project(path)
