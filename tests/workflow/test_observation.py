import pytest
from workflow.observation import run_observation
from workflow.state import WorkflowState, Stage

def test_run_observation(
    mock_decision_dir,
    mock_context,
    mock_cloud_config,
    mocker
):
    mock_query = mocker.patch('workflow.observation.query_claude')
    mock_query.return_value.content = "<test>response</test>"
    
    state = WorkflowState(
        decision_dir=mock_decision_dir,
        context=mock_context,
        stage=Stage.OBSERVE
    )
    
    result = run_observation(state, mock_cloud_config)
    
    assert result == "<test>response</test>"
    assert (mock_decision_dir / "Observation.xml").exists()
    assert mock_query.called
