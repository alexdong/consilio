from typing import Any

class GenerationConfig:
    """Configuration for text generation."""

    def __init__(self, temperature: float | None = None) -> None: ...

class GenerativeModel:
    """A generative AI model."""

    def __init__(
        self, model_name: str, generation_config: dict[str, Any] | None = None,
    ) -> None: ...
    def generate_content(
        self,
        prompt: str,
        generation_config: GenerationConfig | types.GenerationConfig | None = None,
    ) -> Any: ...

class types:
    """Type definitions."""

    class GenerationConfig:
        """Configuration for text generation."""

        def __init__(self, temperature: float | None = None) -> None: ...
