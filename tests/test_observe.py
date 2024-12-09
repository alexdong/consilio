import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from consilio.observe import observe, xml_to_markdown

SAMPLE_XML = """
<observe>
    <observations>
        <observation>Test observation 1</observation>
        <observation>Test observation 2</observation>
    </observations>
    <questions>
        <question>Test question 1?</question>
        <question>Test question 2?</question>
    </questions>
</observe>
"""

@patch('consilio.observe.query_claude')
def test_observe(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = SAMPLE_XML
    mock_query.return_value = mock_response
    
    # Call function
    result = observe(mock_doc, mock_context)
    
    # Verify result
    assert result.startswith("<observe>")
    assert "Test observation" in result
    assert "Test question" in result
    
    # Verify Claude was called correctly
    mock_query.assert_called_once()
    call_args = mock_query.call_args[1]
    assert "DECISION" in call_args["user_prompt"]
    assert mock_context["domain"] in call_args["system_prompt"]
    assert call_args["temperature"] == 0.9

def test_xml_to_markdown():
    markdown = xml_to_markdown(SAMPLE_XML)
    
    # Verify markdown formatting
    assert "## Observations\n" in markdown
    assert "1. Test observation 1" in markdown
    assert "2. Test observation 2" in markdown
    assert "## Questions\n" in markdown
    assert "1. Test question 1?" in markdown
    assert "2. Test question 2?" in markdown
