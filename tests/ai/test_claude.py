import pytest
from ai.claude import query_claude, ClaudeResponse

def test_query_claude(mocker):
    mock_client = mocker.patch('anthropic.Anthropic')
    mock_message = mocker.MagicMock()
    mock_message.content = [mocker.MagicMock(text="Test response")]
    mock_message.model_dump.return_value = {"test": "data"}
    
    mock_client.return_value.messages.create.return_value = mock_message
    
    response = query_claude(
        system_prompt="test system",
        user_prompt="test user",
        api_key="test-key"
    )
    
    assert isinstance(response, ClaudeResponse)
    assert response.content == "Test response"
    assert response.raw == {"test": "data"}
