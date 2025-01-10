import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import re
import tomli
import tomli_w

CONFIG_DIR = Path.home() / ".config" / "consilio"
TOPICS_DIR = Path.home() / ".consilio"


@dataclass
class Topic:
    """Represents a discussion topic with its associated files"""

    slug: str
    created_at: datetime
    description: str

    def __init__(
        self,
        slug: str,
        created_at: datetime,
        description: str,
        test_dir: Optional[Path] = None,
    ):
        self.slug = slug
        self.created_at = created_at
        self.description = description
        self._test_dir = test_dir

    @property
    def directory(self) -> Path:
        """Get the topic's directory path"""
        if self._test_dir is not None:
            return self._test_dir
        return TOPICS_DIR / f"{self.created_at:%Y-%m-%d}-{self.slug}"

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
        return self.directory / f"interview-p{perspective_index}-r{round_num}-response.md"

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
    def create(cls, description: str) -> "Topic":
        """Create a new topic from a description"""
        logger = logging.getLogger("consilio.models")
        logger.info(f"Creating new topic: {description}")
        # Generate a URL-friendly slug from the first line
        first_line = description.split("\n")[0][:50]  # Take first 50 chars
        slug = re.sub(r"[^\w\s-]", "", first_line).strip().lower()
        slug = re.sub(r"[-\s]+", "-", slug)

        topic = cls(slug=slug, created_at=datetime.now(), description=description)

        # Create directory and save description
        topic.directory.mkdir(parents=True, exist_ok=True)
        topic.discussion_file.write_text(description)

        return topic

    @classmethod
    def load(cls, directory: Path) -> Optional["Topic"]:
        """Load a topic from an existing directory"""
        logger = logging.getLogger("consilio.models")
        logger.debug(f"Loading topic from {directory}")
        if not directory.exists():
            return None

        # Parse directory name for date and slug
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-(.*)")
        match = pattern.match(directory.name)
        if match:
            date_str, slug = match.groups()
            created_at = datetime.strptime(date_str, "%Y-%m-%d")
            description = (directory / "discussion.md").read_text()
            return cls(slug=slug, created_at=created_at, description=description)
        return None

    @classmethod
    def list_all(cls) -> List["Topic"]:
        """List all topics in the topics directory"""
        TOPICS_DIR.mkdir(parents=True, exist_ok=True)
        topics = []
        for d in TOPICS_DIR.glob("*-*"):
            if topic := cls.load(d):
                topics.append(topic)
        return sorted(topics, key=lambda t: t.created_at, reverse=True)


class Config:
    """Manages Consilio configuration"""

    def __init__(self, config_path: Optional[Path] = None):
        self.path = config_path if config_path else CONFIG_DIR / "config.toml"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        """Load config from file or create with defaults"""
        if self.path.exists():
            self.data = tomli.loads(self.path.read_text())
        else:
            self.data = {
                "topic": None,
                "key_bindings": "emacs",
                "model": "claude-3-sonnet-20241022",
                "temperature": 1.0,
                "models": {
                    "anthropic": {
                        "default": "claude-3-sonnet-20241022",
                        "models": [
                            "claude-3-sonnet-202401022",
                        ],
                    },
                    "openai": {
                        "default": "gpt-4-turbo-preview",
                        "models": ["gpt-4-turbo-preview"],
                    },
                    "google": {
                        "default": "gemini-2.0-flash-thinking-exp-1219",
                        "models": [
                            "gemini-2.0-flash-thinking-exp-1219",
                            "gemini-2.0-flash-exp",
                        ],
                    },
                },
            }
            self._save()

    def _save(self):
        """Save config to file"""
        self.path.write_text(tomli_w.dumps(self.data))

    @property
    def current_topic(self) -> Optional[Topic]:
        """Get the currently active topic"""
        if not self.data["topic"]:
            return None
        return Topic.load(TOPICS_DIR / self.data["topic"])

    @current_topic.setter
    def current_topic(self, topic: Optional[Topic]):
        """Set the current topic"""
        self.data["topic"] = topic.directory.name if topic else None
        self._save()
