from typing import Dict, Optional
from pathlib import Path
import yaml
from dataclasses import dataclass

@dataclass 
class Context:
    domain: str
    perspective: str
    user_role: str

def load_context(config_path: Optional[Path] = None) -> Context:
    """Load context from yaml file"""
    if not config_path:
        config_path = Path(".consilio.yml")
    
    with open(config_path) as f:
        data = yaml.safe_load(f)
    
    return Context(**data)
