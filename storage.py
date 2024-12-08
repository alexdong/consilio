from pathlib import Path
from datetime import datetime

def create_decision_dir(decision_name: str) -> Path:
    """Create a directory for storing decision-related files
    
    Args:
        decision_name: Name of the decision (usually from the markdown filename)
        
    Returns:
        Path to the created directory
    """
    # Create base decisions directory if it doesn't exist
    decisions_dir = Path("Decisions")
    decisions_dir.mkdir(exist_ok=True)
    
    # Create specific decision directory
    decision_dir = decisions_dir / decision_name
    decision_dir.mkdir(exist_ok=True)
    
    return decision_dir
