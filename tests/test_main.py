import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from consilio.main import main, State, run_repl

@pytest.fixture
def mock_state():
    return State(
        decision_dir=Path("test_decisions"),
        context={
            "domain": "test-domain",
            "user_role": "test-role",
            "perspective": "test-perspective"
        },
        stage="observe",
        doc_path=Path("test.md")
    )

@patch('consilio.main.load_context')
@patch('consilio.main.create_decision_dir')
@patch('consilio.main.observe.observe')
@patch('consilio.main.consult.consult')
@patch('consilio.main.assemble.assemble')
def test_main_initialization(mock_assemble, mock_consult, mock_observe, 
                           mock_create_dir, mock_load_context, tmp_path):
    # Configure mocks
    mock_load_context.return_value = Mock(
        domain="test-domain",
        user_role="test-role",
        perspective="test-perspective"
    )
    mock_create_dir.return_value = tmp_path
    mock_observe.return_value = "Test observation"
    mock_consult.return_value = "Test consultation"
    mock_assemble.return_value = "Test assembly"
    
    # Test with explicit doc path
    doc_path = tmp_path / "test_decision.md"
    doc_path.touch()
    
    with pytest.raises(SystemExit):  # Since we can't easily test the REPL
        main(doc_path=doc_path)
    
    # Verify context was loaded and no real API calls were made
    mock_load_context.assert_called_once()
    mock_create_dir.assert_called_once()
    mock_observe.assert_not_called()  # These should only be called if the REPL runs
    mock_consult.assert_not_called()
    mock_assemble.assert_not_called()

@patch('consilio.main.observe.observe')
@patch('consilio.main.consult.consult')
@patch('consilio.main.assemble.assemble')
def test_run_repl_commands(mock_assemble, mock_consult, mock_observe, mock_state):
    # Configure mocks
    mock_observe.return_value = "Test observation"
    mock_consult.return_value = "Test consultation"
    mock_assemble.return_value = "<perspectives>Test assembly</perspectives>"
    
    # Test observe command
    with patch('prompt_toolkit.PromptSession.prompt', side_effect=['o', KeyboardInterrupt]):
        with pytest.raises(SystemExit):
            run_repl(mock_state)
        mock_observe.assert_called_once()
        mock_assemble.assert_not_called()
        mock_consult.assert_not_called()
    
    # Reset mocks
    mock_observe.reset_mock()
    
    # Test consult command
    with patch('prompt_toolkit.PromptSession.prompt', side_effect=['c', 'y', KeyboardInterrupt]):
        with pytest.raises(SystemExit):
            run_repl(mock_state)
        mock_assemble.assert_called_once()
        mock_consult.assert_called_once()
        mock_observe.assert_not_called()
