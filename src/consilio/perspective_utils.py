import json
import logging
from typing import Any

import click

from consilio.models import Topic


def _display_perspectives(perspectives: list[dict[str, Any]]) -> None:
    """Display available perspectives"""
    click.echo("\nAvailable perspectives:")
    for idx, p in enumerate(perspectives):
        click.echo(f"\n{idx}. {p.get('title', 'Untitled')}")
        click.echo(f"   Expertise: {p.get('expertise', 'N/A')}")


def _get_user_selection(max_choice: int) -> int:
    """Get valid perspective selection from user"""
    while True:
        try:
            choice = click.prompt("\nSelect perspective number", type=int)
            if 0 <= choice < max_choice:
                return choice
            click.echo("Invalid selection. Please try again.")
        except click.Abort:
            msg = "Selection aborted"
            raise click.ClickException(msg) from None


def select_perspective(topic: Topic) -> int:
    """Display perspective selection menu and get user choice"""
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        _display_perspectives(perspectives)
        return _get_user_selection(len(perspectives))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        msg = "No valid perspectives found. Generate perspectives first."
        raise click.ClickException(
            msg,
        ) from e


def get_most_recent_perspective(topic: Topic) -> int | None:
    """Find the most recently interviewed perspective"""
    latest_perspective = None
    latest_round = -1

    # Check all potential perspective files
    for p_idx in range(100):  # reasonable upper limit
        round_num = topic.get_latest_interview_round(p_idx)
        if round_num > latest_round:
            latest_round = round_num
            latest_perspective = p_idx

    return latest_perspective


def get_perspective(topic: Topic, index: int) -> dict[str, Any]:
    """Get a specific perspective by index"""
    logger = logging.getLogger("consilio.interview")
    logger.debug("Getting perspective %s", index)
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        if index < 0 or index >= len(perspectives):
            raise click.ClickException(
                f"Invalid perspective index. Must be between 0 and {len(perspectives) - 1}",
            )
        return perspectives[index]
    except (json.JSONDecodeError, FileNotFoundError) as e:
        msg = "No valid perspectives found. Generate perspectives first."
        raise click.ClickException(
            msg,
        ) from e
