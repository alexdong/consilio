from typing import Any, Optional, Union

class GenerationConfig:
    """Configuration for text generation."""

    def __init__(self, temperature: Optional[float] = None) -> None: ...

class GenerativeModel:
    """A generative AI model."""

    def __init__(
        self, model_name: str, generation_config: Optional[dict[str, Any]] = None
    ) -> None: ...
    def generate_content(
        self,
        prompt: str,
        generation_config: Optional[
            Union["GenerationConfig", "types.GenerationConfig"]
        ] = None,
    ) -> Any: ...

class types:
    """Type definitions."""

    class GenerationConfig:
        """Configuration for text generation."""

        def __init__(self, temperature: Optional[float] = None) -> None: ...
