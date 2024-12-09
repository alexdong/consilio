import pytest
from pathlib import Path


@pytest.fixture
def mock_context():
    return {
        "domain": "test-domain",
        "user_role": "test-role",
        "perspective": "test-perspective",
    }


@pytest.fixture
def mock_doc(tmp_path):
    doc = tmp_path / "test_decision.md"
    doc.write_text("Test decision content")
    return doc
