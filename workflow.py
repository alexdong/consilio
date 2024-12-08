from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

@dataclass
class State:
    """Tracks the current state of the decision-making workflow"""
    decision_dir: Path
    context: Dict[str, str]
    stage: str
    doc_path: Optional[Path] = None
