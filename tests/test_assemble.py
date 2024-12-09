import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from consilio.assemble import assemble, xml_to_markdown

# Test data
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


@patch('consilio.assemble.query_claude')
def test_assemble(mock_query, mock_doc, mock_context):
    # Configure mock
    mock_response = Mock()
    mock_response.content = SAMPLE_XML
    mock_query.return_value = mock_response
    
    # Call function
    result = assemble(mock_doc, mock_context)
    
    # Verify result
    assert result.startswith("<perspectives>")
    assert "Test Perspective" in result
    
    # Verify Claude was called correctly
    mock_query.assert_called_once()
    call_args = mock_query.call_args[1]
    assert "test-domain" in call_args["user_prompt"]
    assert call_args["temperature"] == 0.8

def test_xml_to_markdown():
    markdown = xml_to_markdown(SAMPLE_XML)
    
    # Verify markdown formatting
    assert "## Test Perspective\n" in markdown
    assert "*Test relevance*" in markdown
    assert "- Test question 1?" in markdown
    assert "- Test question 2?" in markdown
