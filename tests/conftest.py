import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict

@pytest.fixture
def test_data_dir(tmp_path) -> Path:
    """Create temporary test data directory"""
    return tmp_path / "test_data"

@pytest.fixture
def mock_decision_dir(test_data_dir) -> Path:
    """Create mock decision directory with required files"""
    decision_dir = test_data_dir / "20240101-test-decision"
    decision_dir.mkdir(parents=True)
    
    # Create Statement.md
    (decision_dir / "Statement.md").write_text("""
# Test Decision
## Summary
Test decision summary
""")
    
    return decision_dir

@pytest.fixture
def mock_cloud_config() -> Dict:
    """Mock cloud configuration"""
    return {
        "claude_key": "test-key",
        "model": "claude-2"
    }

@pytest.fixture
def mock_context() -> Dict[str, str]:
    """Mock context configuration"""
    return {
        "domain": "test domain",
        "perspective": "test perspective",
        "user_role": "Test User"
    }
