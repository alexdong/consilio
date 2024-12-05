import pytest
from workflow.synthesis import run_synthesis
from workflow.state import WorkflowState, Stage

@pytest.mark.asyncio
async def test_run_synthesis(
    mock_decision_dir,
    mock_context,
    mock_cloud_config,
    mocker
):
    # Create test files
    (mock_decision_dir / "Observation.xml").write_text("<test>observation</test>")
    (mock_decision_dir / "Perspectives.xml").write_text("<test>perspectives</test>")
    
    mock_query = mocker.patch('workflow.synthesis.query_claude')
    mock_query.return_value.content = "# Test Synthesis"
    
    state = WorkflowState(
        decision_dir=mock_decision_dir,
        context=mock_context,
        stage=Stage.ADVISE
    )
    
    result = await run_synthesis(state, mock_cloud_config)
    
    assert result == "# Test Synthesis"
    assert (mock_decision_dir / "Memo.md").exists()
    assert mock_query.called
