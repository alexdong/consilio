class GenerationResponse:
    """Response from generate_content."""

    text: str

class GenerationConfig:
    """Configuration for text generation."""

    def __init__(self, temperature: float | None = None) -> None: ...

class GenerativeModel:
    """A generative AI model."""

    def __init__(
        self,
        model_name: str,
        generation_config: dict[str, str | float | int | bool] | None = None,
    ) -> None: ...
    def generate_content(
        self,
        prompt: str,
        generation_config: GenerationConfig | Types.GenerationConfig | None = None,
    ) -> GenerationResponse: ...

class Types:
    """Type definitions."""

    class GenerationConfig:
        """Configuration for text generation."""

        def __init__(self, temperature: float | None = None) -> None: ...
