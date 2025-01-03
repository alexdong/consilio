import click
from pathlib import Path
from typing import Optional
import better_exceptions

better_exceptions.hook()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    """Consilio: AI-Facilitated Decision Making Assistant"""
    pass

@cli.command()
@click.option('-l', '--list', is_flag=True, help='List all topic directories')
@click.option('-t', '--topic-number', type=int, help='Switch to a different topic')
@click.option('-o', '--open', is_flag=True, help='Open topic directory in file explorer')
def topics(list: bool, topic_number: Optional[int], open: bool):
    """Manage discussion topics"""
    click.echo("Topics command")
    # TODO: Implement topics functionality

@cli.command()
@click.option('-e', '--edit', is_flag=True, help='Edit perspectives file')
def perspectives(edit: bool):
    """Manage and generate discussion perspectives"""
    click.echo("Perspectives command")
    # TODO: Implement perspectives functionality

@cli.command()
@click.option('-e', '--edit', type=int, help='Edit specific discussion round')
@click.option('-r', '--round', type=int, help='Restart from specific round')
def discuss(edit: Optional[int], round: Optional[int]):
    """Start or continue discussion rounds"""
    click.echo("Discuss command")
    # TODO: Implement discuss functionality

@cli.command()
@click.argument('shell', type=click.Choice(['bash', 'zsh']), required=False)
def completion(shell: Optional[str]):
    """Generate shell completion scripts for bash or zsh"""
    if shell is None:
        # Print usage if no shell specified
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit(1)
        
    # Get the shell completion script using Click's built-in functionality
    completion_script = click.get_shell_completion(shell)
    click.echo(completion_script)

@cli.command()
def config():
    """Configure Consilio settings"""
    click.echo("Config command")
    # TODO: Implement config functionality


def main():
    """Entry point for the CLI"""
    cli()

if __name__ == "__main__":
    main()
