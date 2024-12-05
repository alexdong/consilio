from pathlib import Path
from datetime import datetime
import shutil
from typing import Optional

def create_decision_dir(title: str) -> Path:
    """Create date-stamped decision directory"""
    date = datetime.now().strftime("%Y%m%d")
    slug = title.lower().replace(" ", "-")
    path = Path(f"Decisions/{date}-{slug}")
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_prompt(stage: str, prompt_type: str) -> str:
    """Load prompt template from Prompts directory"""
    path = Path(f"Prompts/{stage}-{prompt_type}/UserPrompt.md")
    return path.read_text()
