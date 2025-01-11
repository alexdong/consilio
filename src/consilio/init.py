import click
from pathlib import Path


def initialize_project(path: str) -> None:
    """Initialize a new Consilio project in the specified directory"""
    project_dir = Path(path).resolve()

    # Create README.md if it doesn't exist
    readme_path = project_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text("# New Consilio Project\n\nDescribe your topic here.\n")
        click.echo(f"Created README.md in: {project_dir}")
    else:
        click.echo(f"README.md already exists in: {project_dir}")


def handle_init_command(path: str) -> None:
    """Main handler for the init command"""
    initialize_project(path)
