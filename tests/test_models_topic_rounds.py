import pytest
from datetime import datetime
from consilio.models import Topic


@pytest.fixture
def topic_dir(tmp_path):
    """Create a test directory with sample discussion files"""
    # Create test files
    (tmp_path / "round-1-input.md").touch()
    (tmp_path / "round-1-response.md").touch()
    (tmp_path / "round-2-input.md").touch()
    (tmp_path / "interview-1-input.md").touch()
    (tmp_path / "interview-3-response.md").touch()
    return tmp_path


@pytest.fixture
def test_topic(topic_dir):
    """Create a Topic instance with test files"""
    return Topic("test", datetime.now(), "Test description", test_dir=topic_dir)


@pytest.fixture
def empty_topic(tmp_path):
    """Create a Topic instance with no files"""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    return Topic("empty", datetime.now(), "Empty", test_dir=empty_dir)


def test_latest_discussion_round(test_topic):
    """Test getting latest discussion round number"""
    assert test_topic.latest_round == 2


def test_latest_interview_round(test_topic):
    """Test getting latest interview round number"""
    assert test_topic.latest_interview_round == 3


def test_empty_directory_rounds(empty_topic):
    """Test round numbers with no files present"""
    assert empty_topic.latest_round == 0
    assert empty_topic.latest_interview_round == 0


def test_invalid_filenames(test_topic, topic_dir):
    """Test round numbers with invalid filenames present"""
    # Add invalid files
    (topic_dir / "round-invalid-input.md").touch()
    (topic_dir / "interview-bad-response.md").touch()
    
    # Should ignore invalid files
    assert test_topic.latest_round == 2
    assert test_topic.latest_interview_round == 3
