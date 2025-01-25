import json
import re
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


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

def display_perspectives(perspectives: List[Perspective]) -> None:
    """Display perspectives in markdown format using rich"""
    console = Console()

    # Convert perspectives to Perspective objects if they're dicts
    perspectives = [Perspective.model_validate(p) for p in perspectives]

    # Build markdown content from Perspective objects
    md_content = "".join(p.to_markdown(i) for i, p in enumerate(perspectives, 1))

    # Display using rich
    console.print(Markdown(md_content))



class Clarification(BaseModel):
    """Represents a clarification response with its sections"""

    questions: List[str]
    missing_context: List[str]
    assumptions: List[str]
    suggestions: List[str]

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


class BiasAnalysis(BaseModel):
    """Represents a bias analysis response"""

    cognitive_biases: List[str]
    emotional_biases: List[str]
    cultural_biases: List[str]
    professional_biases: List[str]
    recommendations: List[str]

    def to_markdown(self) -> str:
        """Convert bias analysis to markdown format"""
        md = "\n"

        md += "__Cognitive Biases__\n"
        for bias in self.cognitive_biases:
            md += f"* {bias}\n"
        md += "\n"

        md += "__Emotional Biases__\n"
        for bias in self.emotional_biases:
            md += f"* {bias}\n"
        md += "\n"

        md += "__Cultural/Social Biases__\n"
        for bias in self.cultural_biases:
            md += f"* {bias}\n"
        md += "\n"

        md += "__Professional Biases__\n"
        for bias in self.professional_biases:
            md += f"* {bias}\n"
        md += "\n"

        md += "__Recommendations__\n"
        for rec in self.recommendations:
            md += f"* {rec}\n"
        md += "\n"

        return md

    @classmethod
    def from_dict(cls, data: dict) -> "BiasAnalysis":
        """Create a BiasAnalysis instance from a dictionary"""
        return cls(**data)


class StressAnalysis(BaseModel):
    """Represents a stress test analysis response"""

    failure_points: List[str]
    edge_cases: List[str]
    hidden_assumptions: List[str]
    resource_constraints: List[str]
    mitigation_strategies: List[str]

    def to_markdown(self) -> str:
        """Convert stress analysis to markdown format"""
        md = "__Stress Test Analysis__\n\n"

        md += "__Potential Failure Points__\n"
        for point in self.failure_points:
            md += f"* {point}\n"
        md += "\n"

        md += "__Critical Edge Cases__\n"
        for case in self.edge_cases:
            md += f"* {case}\n"
        md += "\n"

        md += "__Hidden Assumptions__\n"
        for assumption in self.hidden_assumptions:
            md += f"* {assumption}\n"
        md += "\n"

        md += "__Resource Constraints__\n"
        for constraint in self.resource_constraints:
            md += f"* {constraint}\n"
        md += "\n"

        md += "__Mitigation Strategies__\n"
        for strategy in self.mitigation_strategies:
            md += f"* {strategy}\n"
        md += "\n"

        return md

    @classmethod
    def from_dict(cls, data: dict) -> "StressAnalysis":
        """Create a StressAnalysis instance from a dictionary"""
        return cls(**data)


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


class Summary(BaseModel):
    """Represents a discussion summary"""

    key_points: List[str]
    decisions: List[str]
    open_questions: List[str]
    next_steps: List[str]

    def to_markdown(self) -> str:
        """Convert summary to markdown format"""
        md = "__Discussion Summary__\n\n"

        md += "__Key Points__\n"
        for point in self.key_points:
            md += f"* {point}\n"
        md += "\n"

        md += "__Decisions__\n"
        for decision in self.decisions:
            md += f"* {decision}\n"
        md += "\n"

        md += "__Open Questions__\n"
        for question in self.open_questions:
            md += f"* {question}\n"
        md += "\n"

        md += "__Next Steps__\n"
        for step in self.next_steps:
            md += f"* {step}\n"
        md += "\n"

        return md

    @classmethod
    def from_dict(cls, data: dict) -> "Summary":
        """Create a Summary instance from a dictionary"""
        return cls(**data)


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
    def perspectives(self) -> List[Perspective]:
        """Get the list of perspectives"""
        try:
            with open(self.perspectives_file) as f:
                data = json.load(f)
            return [Perspective.model_validate(p) for p in data]
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
