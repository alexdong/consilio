import click
from typing import Optional
import better_exceptions
from consilio.version import __version__
from consilio.topics import handle_topics_command
from consilio.perspectives import handle_perspectives_command
from consilio.discuss import handle_discuss_command
from consilio.interview import handle_interview_command
from consilio.config import handle_config_command

better_exceptions.hook()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="consilio")
def cli():
    """Consilio: AI-Facilitated Decision Making Assistant"""
    pass


@cli.command()
@click.option("-l", "--list", is_flag=True, help="List all topic directories")
@click.option("-t", "--topic-number", type=int, help="Switch to a different topic")
@click.option(
    "-o", "--open", is_flag=True, help="Open topic directory in file explorer"
)
def topics(list: bool, topic_number: Optional[int], open: bool):
    """Manage discussion topics"""
    handle_topics_command(list, topic_number, open)


@cli.command()
@click.option("-e", "--edit", is_flag=True, help="Edit perspectives file")
@click.option("-l", "--list", is_flag=True, help="List all perspectives")
def perspectives(edit: bool, list_flag: bool):
    """Manage and generate discussion perspectives"""
    handle_perspectives_command(edit, list_flag)


@cli.command()
@click.option("-e", "--edit", type=int, help="Edit specific discussion round")
@click.option("-r", "--round", type=int, help="Restart from specific round")
def discuss(edit: Optional[int], round: Optional[int]):
    """Start or continue discussion rounds"""
    handle_discuss_command(edit, round)


@cli.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]), required=False)
def completion(shell: Optional[str]):
    """Generate shell completion scripts for bash or zsh"""
    if shell is None:
        # Print usage if no shell specified
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit(1)

    if shell == "bash":
        click.echo(message="Add the following line to your .bashrc or .bash_profile:")
        click.echo(message='eval "$(_CONS_COMPLETE=bash_source consilio)"')
    elif shell == "zsh":
        click.echo(message="Add the following line to your .zshrc:")
        click.echo(message='eval "$(_CONS_COMPLETE=zsh_source consilio)"')
    elif shell == "fish":
        click.echo("Add this to ~/.config/fish/completions/foo-bar.fish")
        click.echo("_CONS_COMPLETE=fish_source cons | source)")
    else:
        click.echo("Invalid shell specified. Please use 'bash' or 'zsh'.")


@cli.command()
@click.argument("perspective_index", type=int)
@click.option("-r", "--round", type=int, help="Start from specific round")
def interview(perspective_index: int, round: Optional[int]):
    """Interview a specific perspective"""
    handle_interview_command(perspective_index, round)


@cli.command()
def config():
    """Configure Consilio settings"""
    handle_config_command()


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
