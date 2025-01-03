from datetime import datetime
from pathlib import Path
import pytest
from consilio.models import Topic

def test_get_latest_round_number(tmp_path):
    # Create a test topic
    topic = Topic("test", datetime.now(), "Test description")
    topic.directory = tmp_path  # Override directory for testing
    
    # Create some test files
    (tmp_path / "round-1-input.md").touch()
    (tmp_path / "round-1-response.md").touch()
    (tmp_path / "round-2-input.md").touch()
    (tmp_path / "interview-1-input.md").touch()
    (tmp_path / "interview-3-response.md").touch()
    
    # Test regular discussion rounds
    assert topic.latest_round == 2
    
    # Test interview rounds
    assert topic.latest_interview_round == 3
    
    # Test with no matching files
    empty_topic = Topic("empty", datetime.now(), "Empty")
    empty_topic.directory = tmp_path / "empty"
    empty_topic.directory.mkdir()
    assert empty_topic.latest_round == 0
    assert empty_topic.latest_interview_round == 0
    
    # Test with invalid filenames
    (tmp_path / "round-invalid-input.md").touch()
    (tmp_path / "interview-bad-response.md").touch()
    assert topic.latest_round == 2  # Should ignore invalid files
    assert topic.latest_interview_round == 3
