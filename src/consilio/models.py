import json
import re
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown


class Perspective(BaseModel):
    """Represents a single perspective with its attributes"""

    title: str
    expertise: str
    goal: str
    role: str

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


def display_perspectives(perspectives: list[Perspective]) -> None:
    """Display perspectives in markdown format using rich"""
    console = Console()

    # Build markdown content from Perspective objects
    md_content = "".join(
        Perspective(**p).to_markdown(i) for i, p in enumerate(perspectives, 1)
    )

    # Display using rich
    console.print(Markdown(md_content))


class Clarification(BaseModel):
    """Represents a clarification response with its sections"""

    questions: list[str]
    missing_context: list[str]
    assumptions: list[str]
    suggestions: list[str]

    def to_markdown(self) -> str:
        """Convert clarification to markdown format"""
        md = "__Questions__\n"

        if self.questions:
            for i, q in enumerate(self.questions, 1):
                md += f"{i}. {q}\n"
            md += "\n"

        if self.missing_context:
            md += "__Missing Context__\n"
            for item in self.missing_context:
                md += f"* {item}\n"
            md += "\n"

        if self.assumptions:
            md += "__Assumptions to Verify__\n"
            for item in self.assumptions:
                md += f"* {item}\n"
            md += "\n"

        if self.suggestions:
            md += "__Suggestions__\n"
            for item in self.suggestions:
                md += f"* {item}\n"
            md += "\n"

        return md

    def to_json(self) -> dict:
        """Convert clarification to JSON-compatible dictionary"""
        return self.model_dump()


class Discussion(BaseModel):
    """Represents a discussion response"""

    perspective: str
    opinion: str

    def to_markdown(self) -> str:
        """Convert discussion to markdown format"""
        return f"**{self.perspective}:**\n{self.opinion}\n\n"

    @classmethod
    def from_dict(cls, data: dict) -> "Discussion":
        """Create a Discussion instance from a dictionary"""
        return cls(**data)


def display_discussions(discussion_list: list[dict[str, str]]) -> None:
    """Display discussion in markdown format using rich"""
    console = Console()

    # Convert to Discussion objects if they're dicts
    discussions = [Discussion.from_dict(d) for d in discussion_list]

    # Build markdown content from Discussion objects
    md_content = "## Discussion Round\n\n" + "".join(
        d.to_markdown() for d in discussions
    )

    # Display using rich
    console.print(Markdown(md_content))


def display_interview(interview: dict) -> None:
    """Display interview response in markdown format"""
    console = Console()
    md_content = "## Interview Response\n\n" + interview["opinion"]
    console.print(Markdown(md_content))


class Config(BaseModel):
    """Configuration settings for a topic"""

    key_bindings: str = Field(
        default="emacs", description="Key bindings style (emacs or vi)"
    )
    model: str = Field(default="gemini-2.0-flash-exp", description="Model identifier")
    temperature: float = Field(
        default=0.5, description="Temperature for model responses"
    )

    def save(self, path: Optional[Path] = None) -> None:
        """Save config to file"""
        path = path or Path("cons.toml")
        path.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Config":
        """Load config from file"""
        path = path or Path("cons.toml")
        if path.exists():
            return cls.model_validate_json(path.read_text())
        return cls()


class Topic(BaseModel):
    """Represents a discussion topic with its associated files"""

    dir_path: Path = Field(default_factory=lambda: Path("."))
    config: Config = Field(default_factory=Config)

    @property
    def directory(self) -> Path:
        """Get the topic's directory path"""
        return self.dir_path

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

    def discussion_input_file(self, round_num: int) -> Path:
        """Get the path for a specific round's input file"""
        return self.directory / f"discussion-r{round_num}-input.md"

    def discussion_response_file(self, round_num: int) -> Path:
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
        pattern = re.compile(rf"{prefix}(\d+)-response\.md")
        rounds = []
        for f in self.directory.glob(f"{prefix}*-*.md"):
            match = pattern.match(f.name)
            if match and match.group(1):
                rounds.append(int(match.group(1)))
        return max(rounds) if rounds else 0

    @property
    def description(self) -> str:
        """Get the topic's description"""
        return self.discussion_file.read_text()

    @property
    def perspectives(self) -> list[Perspective]:
        """Get the list of perspectives"""
        try:
            with open(self.perspectives_file) as f:
                data = json.load(f)
            return [Perspective(**p) for p in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @property
    def latest_discussion_round(self) -> int:
        """Get the number of the latest discussion round"""
        return self._get_latest_round_number("discussion-r")

    def get_latest_interview_round(self, perspective_index) -> int:
        """Get the number of the latest interview round"""
        return self._get_latest_round_number(f"interview-p{perspective_index}-r")

    @classmethod
    def create(cls) -> "Topic":
        """Create a new topic"""
        return cls()

    @classmethod
    def load(cls) -> "Topic":
        """Load topic from current directory"""
        return cls()
