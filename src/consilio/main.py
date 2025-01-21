import click
import logging
from pathlib import Path
from typing import Optional
import better_exceptions
from consilio.logging import setup_logging
from consilio.version import __version__
from consilio.init import handle_init_command
from consilio.perspectives import handle_perspectives_command
from consilio.interview import handle_interview_command
from consilio.discuss import handle_discuss_command
from consilio.clarify import handle_clarify_command
from consilio.stress import handle_stress_command
from consilio.bias import handle_bias_command
from consilio.summary import handle_summary_command

better_exceptions.hook()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="consilio")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="DEBUG",
    help="Set logging level",
)
@click.option(
    "--log-file", type=click.Path(path_type=Path), help="Write logs to specified file"
)
def cli(log_level: str, log_file: Optional[Path]):
    """Consilio: AI-Facilitated Decision Making Assistant"""
    setup_logging(log_level, log_file)
    logger = logging.getLogger("consilio.cli")
    logger.debug("CLI started")


@cli.command()
def init():
    """Initialize a new Consilio project in the specified directory"""
    handle_init_command()


@cli.command()
def clarify():
    """Request clarification before discussion"""
    handle_clarify_command()

@cli.command()
def perspectives():
    """Generate, add, or edit perspectives for the current topic"""
    handle_perspectives_command()

@cli.command()
def interview():
    """Start or continue interview rounds"""
    handle_interview_command()

@cli.command()
@click.option("-r", "--round", type=int, help="Restart from specific round")
def discuss(round: Optional[int]):
    """Start or continue discussion rounds"""
    handle_discuss_command(round)

@cli.command()
def stress():
    """Stress test current discussion and decisions"""
    handle_stress_command()


@cli.command()
def bias():
    """Check for cognitive and other biases"""
    handle_bias_command()


@cli.command()
def summary():
    """Generate comprehensive discussion summary"""
    handle_summary_command()


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


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
