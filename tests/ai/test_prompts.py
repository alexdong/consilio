import pytest
from pathlib import Path
from ai.prompts import load_prompt_template, format_prompt

def test_load_prompt_template(tmp_path):
    # Create test prompts
    prompt_dir = tmp_path / "Prompts/1-Observe"
    prompt_dir.mkdir(parents=True)
    
    (prompt_dir / "SystemPrompt.md").write_text("System {{test}}")
    (prompt_dir / "UserPrompt.md").write_text("User {{test}}")
    
    with pytest.MonkeyPatch.context() as m:
        m.chdir(tmp_path)
        template = load_prompt_template("1-Observe")
        
        assert template.system == "System {{test}}"
        assert template.user == "User {{test}}"

def test_format_prompt():
    template = "Hello {{name}}!"
    context = {"name": "World"}
    
    result = format_prompt(template, context)
    assert result == "Hello World!"

def test_format_prompt_missing_var():
    template = "Hello {{name}}!"
    context = {}
    
    result = format_prompt(template, context)
    assert result == "Hello {{name}}!"
