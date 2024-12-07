import pytest
from ai.claude import query_claude, ClaudeResponse
import anthropic


def test_query_claude_basic(mocker):
    """Test basic successful query"""
    mock_client = mocker.patch("anthropic.Anthropic")
    mock_message = mocker.MagicMock()
    mock_message.content = [mocker.MagicMock(text="Test response")]
    mock_message.model_dump.return_value = {"test": "data"}

    mock_client.return_value.messages.create.return_value = mock_message

    response = query_claude(
        system_prompt="test system",
        user_prompt="test user"
    )

    assert isinstance(response, ClaudeResponse)
    assert response.content == "Test response"
    assert response.raw == {"test": "data"}

    # Verify correct parameters were passed
    mock_client.return_value.messages.create.assert_called_once_with(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0.7,
        system="test system",
        messages=[
            {
                "role": "user",
                "content": "test user",
            },
            {
                "role": "assistant",
                "content": [],
            },
        ],
    )


def test_query_claude_with_assistant(mocker):
    """Test query with assistant message"""
    mock_client = mocker.patch("anthropic.Anthropic")
    mock_message = mocker.MagicMock()
    mock_message.content = [mocker.MagicMock(text="Test response")]
    mock_message.model_dump.return_value = {"test": "data"}

    mock_client.return_value.messages.create.return_value = mock_message

    response = query_claude(
        system_prompt="test system",
        user_prompt="test user",
        assistant="previous response",
        temperature=0.9
    )

    assert isinstance(response, ClaudeResponse)
    assert response.content == "Test response"

    # Verify assistant message was included
    mock_client.return_value.messages.create.assert_called_once_with(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0.9,
        system="test system",
        messages=[
            {
                "role": "user",
                "content": "test user",
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "previous response"}],
            },
        ],
    )


def test_query_claude_multiple_content_blocks(mocker):
    """Test handling multiple content blocks in response"""
    mock_client = mocker.patch("anthropic.Anthropic")
    mock_message = mocker.MagicMock()
    mock_message.content = [
        mocker.MagicMock(text="First block"),
        mocker.MagicMock(text=" Second block"),
        mocker.MagicMock(text=" Third block")
    ]
    mock_message.model_dump.return_value = {"test": "data"}

    mock_client.return_value.messages.create.return_value = mock_message

    response = query_claude(
        system_prompt="test system",
        user_prompt="test user"
    )

    assert response.content == "First block Second block Third block"


def test_query_claude_api_error(mocker):
    """Test handling of API errors"""
    mock_client = mocker.patch("anthropic.Anthropic")
    mock_client.return_value.messages.create.side_effect = anthropic.APIError(
        message="API Error",
        http_status=500,
        http_body="Internal Server Error"
    )

    with pytest.raises(anthropic.APIError) as exc_info:
        query_claude(
            system_prompt="test system",
            user_prompt="test user"
        )
    
    assert "API Error" in str(exc_info.value)


def test_query_claude_missing_api_key(mocker):
    """Test handling of missing API key"""
    mocker.patch.dict('os.environ', clear=True)
    
    with pytest.raises(KeyError) as exc_info:
        query_claude(
            system_prompt="test system",
            user_prompt="test user"
        )
    
    assert "ANTHROPIC_API_KEY" in str(exc_info.value)
