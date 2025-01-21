import click
import json
import logging
from typing import Optional
from consilio.models import Topic

def select_perspective(topic: Topic) -> int:
    """Display perspective selection menu and get user choice"""
    try:
        perspectives = json.loads(topic.perspectives_file.read_text())
        click.echo("\nAvailable perspectives:")
        for idx, p in enumerate(perspectives):
            click.echo(f"\n{idx}. {p.get('title', 'Untitled')}")
            click.echo(f"   Expertise: {p.get('expertise', 'N/A')}")
        
        while True:
            try:
                choice = click.prompt("\nSelect perspective number", type=int)
                if 0 <= choice < len(perspectives):
                    return choice
                click.echo("Invalid selection. Please try again.")
            except click.Abort:
                raise click.ClickException("Selection aborted")
    except (json.JSONDecodeError, FileNotFoundError):
        raise click.ClickException("No valid perspectives found. Generate perspectives first.")

def get_most_recent_perspective(topic: Topic) -> Optional[int]:
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
