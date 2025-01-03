from typing import Any, Dict, Optional

class GenerationConfig:
    """Configuration for text generation."""
    def __init__(self, temperature: Optional[float] = None) -> None: ...

class GenerativeModel:
    """A generative AI model."""
    def __init__(self, model_name: str, generation_config: Optional[Dict[str, Any]] = None) -> None: ...
    
    def generate_content(
        self, 
        prompt: str,
        generation_config: Optional[GenerationConfig] = None
    ) -> Any: ...

class types:
    """Type definitions."""
    class GenerationConfig(GenerationConfig): ...
