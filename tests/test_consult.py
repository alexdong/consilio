import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from consilio.consult import consult, get_perspective_opinion

SAMPLE_XML = """
<perspectives>
    <perspective>
        <title>Test Perspective</title>
        <relevance>Test relevance</relevance>
        <questions>
            <question>Test question 1?</question>
            <question>Test question 2?</question>
        </questions>
    </perspective>
</perspectives>
"""

SAMPLE_OPINION = "This is a test opinion from the perspective."

@patch('consilio.consult.query_claude')
def test_get_perspective_opinion(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = SAMPLE_OPINION
    mock_query.return_value = mock_response
    
    # Call function
    result = get_perspective_opinion(
        doc=mock_doc,
        title="Test Perspective",
        user_prompt="test prompt",
        assistant_prefix="test prefix",
        perspective_title="Test Perspective"
    )
    
    # Verify result
    assert result == SAMPLE_OPINION
    
    # Verify Claude was called correctly
    mock_query.assert_called_once()
    call_args = mock_query.call_args[1]
    assert call_args["user_prompt"] == "test prompt"
    assert call_args["assistant"] == "test prefix"
    assert call_args["temperature"] == 0.8

def test_consult(mock_doc, mock_context):
    result = consult(mock_doc, SAMPLE_XML, mock_context)
    
    # Verify result structure
    assert result.startswith("<opinions>")
    assert result.endswith("</opinions>")
    assert "<opinion>" in result
