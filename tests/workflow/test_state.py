import pytest
from pathlib import Path
from workflow.state import WorkflowState, Stage

def test_workflow_state_init(mock_decision_dir, mock_context):
    state = WorkflowState(
        decision_dir=mock_decision_dir,
        context=mock_context,
        stage=Stage.OBSERVE
    )
    
    assert state.decision_dir == mock_decision_dir
    assert state.context == mock_context
    assert state.stage == Stage.OBSERVE
    assert state.perspectives == []

def test_workflow_state_advance():
    state = WorkflowState(
        decision_dir=Path(),
        context={},
        stage=Stage.OBSERVE
    )
    
    state.advance_stage()
    assert state.stage == Stage.CONSULT
    
    state.advance_stage()
    assert state.stage == Stage.ADVISE
