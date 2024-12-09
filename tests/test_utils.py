import pytest
from consilio.utils import generate_interaction_filename


from unittest.mock import Mock
from consilio.utils import escape_xml_string, ClaudeResponse

def test_generate_interaction_filename(freezer):
    # Freeze time to 2024-01-01 12:34:56
    freezer.move_to("2024-01-01 12:34:56")

    # Test basic filename generation
    filename = generate_interaction_filename("observe")
    assert filename == "240101_123456-observe.md"

    # Test filename with perspective
    filename = generate_interaction_filename("consult", "Test Perspective")
    assert filename == "240101_123456-consult_Test_Perspective.md"

def test_escape_xml_string():
    # Test basic XML escaping
    assert escape_xml_string("test & test") == "test &amp; test"
    assert escape_xml_string(" test ") == "test"  # Tests strip()

def test_claude_response():
    # Test ClaudeResponse dataclass
    raw_response = {"content": "test", "other": "data"}
    response = ClaudeResponse(content="test", raw=raw_response)
    assert response.content == "test"
    assert response.raw == raw_response
