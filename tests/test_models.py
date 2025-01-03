from datetime import datetime
from pathlib import Path
import pytest
from consilio.models import Topic

def test_get_latest_round_number(tmp_path):
    # Create a test topic with test directory
    topic = Topic("test", datetime.now(), "Test description", test_dir=tmp_path)
    
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
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    empty_topic = Topic("empty", datetime.now(), "Empty", test_dir=empty_dir)
    empty_topic.directory.mkdir()
    assert empty_topic.latest_round == 0
    assert empty_topic.latest_interview_round == 0
    
    # Test with invalid filenames
    (tmp_path / "round-invalid-input.md").touch()
    (tmp_path / "interview-bad-response.md").touch()
    assert topic.latest_round == 2  # Should ignore invalid files
    assert topic.latest_interview_round == 3
