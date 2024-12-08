import asyncio
import click
from pathlib import Path
from typing import Optional

from utils import load_context
from cloud import init_cloud
from workflow import WorkflowState, observe
from storage import create_decision_dir


@click.command()
@click.option("--context", type=Path, help="Path to context file")
def main(context: Optional[Path]) -> None:
    """Main entry point for Consilio"""
    print("[🤔] Initializing Consilio...")

    ctx = load_context(context)
    cloud_cfg = init_cloud()

    decision_type = click.prompt("Decision type", type=str)
    title = click.prompt("Decision title", type=str)

    decision_dir = create_decision_dir(title)

    state = WorkflowState(
        decision_dir=decision_dir, context={"type": decision_type}, stage="observe"
    )

    asyncio.run(observe(state))


if __name__ == "__main__":
    main()
