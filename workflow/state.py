from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List
from enum import Enum

class Stage(Enum):
    OBSERVE = "1-Observe"
    CONSULT = "2-Consult"
    ADVISE = "3-Advise"

@dataclass
class WorkflowState:
    decision_dir: Path
    context: Dict[str, str]
    stage: Stage
    observation: Optional[str] = None
    perspectives: List[str] = None
    
    def __post_init__(self):
        if self.perspectives is None:
            self.perspectives = []

    def advance_stage(self) -> None:
        """Move to next workflow stage"""
        if self.stage == Stage.OBSERVE:
            self.stage = Stage.CONSULT
        elif self.stage == Stage.CONSULT:
            self.stage = Stage.ADVISE
