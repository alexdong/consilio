import pytest
from workflow.consultation import run_consultation, extract_perspectives
from workflow.state import WorkflowState, Stage

def test_extract_perspectives():
    xml = """
    <root>
        <perspective>
            <title>Test Title</title>
            <question>Test Question</question>
        </perspective>
    </root>
    """
    
    perspectives = extract_perspectives(xml)
    assert len(perspectives) == 1
    assert perspectives[0]["title"] == "Test Title"
    assert perspectives[0]["question"] == "Test Question"

def test_run_consultation(
    mock_decision_dir,
    mock_context,
    mock_cloud_config,
    mocker
):
    # Create test observation file
    observation = """
    <root>
        <perspective>
            <title>Test Perspective</title>
            <question>Test Question</question>
        </perspective>
    </root>
    """
    (mock_decision_dir / "Observation.xml").write_text(observation)
    
    mock_query = mocker.patch('workflow.consultation.query_claude')
    mock_query.return_value.content = "<response>test</response>"
    
    state = WorkflowState(
        decision_dir=mock_decision_dir,
        context=mock_context,
        stage=Stage.CONSULT
    )
    
    results = run_consultation(state, mock_cloud_config)
    
    assert len(results) == 1
    assert results[0] == "<response>test</response>"
    assert (mock_decision_dir / "Perspectives.xml").exists()
