import logging
import re
import tomli
import tomli_w
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional


@dataclass
class Perspective:
    """Represents a single perspective with its attributes"""

    title: str
    expertise: str
    goal: str
    role: str

    @classmethod
    def from_dict(cls, data: dict) -> "Perspective":
        """Create a Perspective instance from a dictionary"""
        return cls(
            title=data.get("Title", "Unnamed Perspective"),
            expertise=data.get("Expertise", ""),
            goal=data.get("Goal", ""),
            role=data.get("Role", ""),
        )

    def to_markdown(self, index: int) -> str:
        """Convert perspective to markdown format"""
        md = f"__{index}. {self.title}__\n"
        if self.expertise:
            md += f"* **Expertise:** {self.expertise}\n"
        if self.goal:
            md += f"* **Goal:** {self.goal}\n"
        if self.role:
            md += f"* **Role:** {self.role}\n"
        md += "\n"
        return md

    def to_json(self) -> dict:
        """Convert perspective to JSON format"""
        return {
            "Title": self.title,
            "Expertise": self.expertise,
            "Goal": self.goal,
            "Role": self.role
        }


@dataclass
class Clarification:
    """Represents a clarification response with its sections"""

    questions: List[str]
    missing_context: List[str]
    assumptions: List[str]
    suggestions: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Clarification":
        """Create a Clarification instance from a dictionary"""
        return cls(
            questions=data.get("questions", []),
            missing_context=data.get("missing_context", []),
            assumptions=data.get("assumptions", []),
            suggestions=data.get("suggestions", []),
        )

    def to_markdown(self) -> str:
        """Convert clarification to markdown format"""
        md = "__Questions__"

        # Questions section
        if self.questions:
            for i, q in enumerate(self.questions, 1):
                md += f"{i}. {q}\n"
            md += "\n"

        # Missing Context section
        if self.missing_context:
            md += "__Missing Context__\n"
            for item in self.missing_context:
                md += f"* {item}\n"
            md += "\n"

        # Assumptions section
        if self.assumptions:
            md += "__Assumptions to Verify__\n"
            for item in self.assumptions:
                md += f"* {item}\n"
            md += "\n"

        # Suggestions section
        if self.suggestions:
            md += "__Suggestions__\n"
            for item in self.suggestions:
                md += f"* {item}\n"
            md += "\n"

        return md

    def to_json(self) -> dict:
        """Convert clarification to JSON format"""
        return {
            "questions": self.questions,
            "missing_context": self.missing_context,
            "assumptions": self.assumptions,
            "suggestions": self.suggestions
        }


@dataclass
class Config:
    """Configuration settings for a topic"""

    key_bindings: str = "emacs"  # or "vi"
    model: str = "claude-3-5-sonnet-20241022"
    temperature: float = 1.0

    def __post_init__(self) -> None:
        """Write config to cons.toml if it doesn't exist"""
        config_file = Path("cons.toml")
        if not config_file.exists():
            config = {
                "key_bindings": self.key_bindings,
                "model": self.model,
                "temperature": self.temperature,
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
    def config_file(self) -> Path:
        """Get the cons.toml file path"""
        return self.directory / "cons.toml"

    @property
    def discussion_file(self) -> Path:
        """Get the discussion.md file path"""
        return self.directory / "README.md"

    @property
    def perspectives_file(self) -> Path:
        """Get the perspectives.md file path"""
        return self.directory / "perspectives.json"

    @property
    def clarification_answers_file(self) -> Path:
        """Get the clarification_answers.md file path"""
        return self.directory / "clarification.json"

    def round_input_file(self, round_num: int) -> Path:
        """Get the path for a specific round's input file"""
        return self.directory / f"discussion-r{round_num}-input.md"

    def round_response_file(self, round_num: int) -> Path:
        """Get the path for a specific round's response file"""
        return self.directory / f"discussion-r{round_num}-response.md"

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
    def description(self) -> str:
        """Get the topic's description"""
        return self.discussion_file.read_text()

    @property
    def perspectives(self) -> List[Perspective]:
        """Get the list of perspectives"""
        try:
            with open(self.perspectives_file) as f:
                data = json.load(f)
            return [Perspective.from_dict(p) for p in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

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
        return cls()
