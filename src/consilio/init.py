import click
import subprocess
from pathlib import Path
from .utils import render_template


def handle_init_command(path: str = ".") -> None:
    """Initialize a new project and open README.md in editor"""
    project_dir = Path(path).resolve()
    readme_path = project_dir / "README.md"

    if not readme_path.exists():
        content = render_template("edit.j2")
        readme_path.write_text(content)
        click.echo(f"Created README.md in: {project_dir}")
    else:
        content = readme_path.read_text()

    try:
        click.edit(
            text=content,
            filename=str(readme_path),
        )
    except subprocess.SubprocessError:
        click.echo(f"Failed to open {readme_path} in editor")
