import click
import logging
import re
import tomli
import tomli_w
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Any

@dataclass
class Config:
    """Configuration settings for a topic"""
    key_bindings: str = "emacs"  # or "vi"
    model: str = "claude-3-sonnet-20240229"
    temperature: float = 1.0

    def __post_init__(self) -> None:
        """Write config to cons.toml if it doesn't exist"""
        config_file = Path("cons.toml")
        if not config_file.exists():
            config = {
                "key_bindings": self.key_bindings,
                "model": self.model,
                "temperature": self.temperature
            }
            config_file.write_text(tomli_w.dumps(config))

    def __getattribute__(self, name: str) -> Any:
        """Load config from cons.toml before accessing attributes"""
        config_file = Path("cons.toml")
        if config_file.exists():
            config = tomli.loads(config_file.read_text())
            if name in config:
                return config[name]
        return super().__getattribute__(name)


@dataclass
class Topic:
    """Represents a discussion topic with its associated files"""

    def __init__(self, dir: Path = Path(".")):
        self._dir = dir
        self.config = Config()

    @property
    def directory(self) -> Path:
        """Get the topic's directory path"""
        return self._dir

    @property
    def discussion_file(self) -> Path:
        """Get the discussion.md file path"""
        return self.directory / "discussion.md"

    @property
    def perspectives_file(self) -> Path:
        """Get the perspectives.md file path"""
        return self.directory / "perspectives.md"

    @property
    def clarification_file(self) -> Path:
        """Get the clarification.json file path"""
        return self.directory / "clarification.json"

    @property
    def clarification_answers_file(self) -> Path:
        """Get the clarification_answers.md file path"""
        return self.directory / "clarification_answers.md"

    def round_input_file(self, round_num: int) -> Path:
        """Get the path for a specific round's input file"""
        return self.directory / f"round-{round_num}-input.md"

    def round_response_file(self, round_num: int) -> Path:
        """Get the path for a specific round's response file"""
        return self.directory / f"round-{round_num}-response.md"

    def interview_input_file(self, perspective_index: int, round_num: int) -> Path:
        """Get the path for a specific interview round's input file"""
        return self.directory / f"interview-p{perspective_index}-r{round_num}-input.md"

    def interview_response_file(self, perspective_index: int, round_num: int) -> Path:
        """Get the path for a specific interview round's response file"""
        return (
            self.directory / f"interview-p{perspective_index}-r{round_num}-response.md"
        )

    def _get_latest_round_number(self, prefix: str) -> int:
        """Get the latest round number for a given file prefix (round/interview)"""
        logger = logging.getLogger("consilio.models")
        logger.debug(f"Getting latest {prefix} round number")
        pattern = re.compile(rf"{prefix}-(\d+)-(?:input|response)\.md")
        rounds = []
        for f in self.directory.glob(f"{prefix}-*-*.md"):
            match = pattern.match(f.name)
            if match and match.group(1):
                rounds.append(int(match.group(1)))
        return max(rounds) if rounds else 0

    @property
    def latest_round(self) -> int:
        """Get the number of the latest discussion round"""
        return self._get_latest_round_number("round")

    @property
    def latest_interview_round(self) -> int:
        """Get the number of the latest interview round"""
        return self._get_latest_round_number("interview")

    @classmethod
    def create(cls) -> "Topic":
        """Create a new topic"""
        return cls()

    @classmethod
    def load(cls) -> "Topic":
        """Load topic from current directory"""
        if Path("README.md").exists():
            return cls()
        raise click.ClickException(
            "No topic selected. Use 'cons topics -t <number>' to select one."
        )
