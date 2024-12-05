from typing import Optional, Union
import os
import tempfile
import subprocess
from pathlib import Path

def get_editor_input(
    initial_text: str = "",
    editor: Optional[str] = None,
    suffix: str = ".md",
    encoding: str = "utf-8",
    delete: bool = True,
    dir: Optional[Union[str, Path]] = None
) -> str:
    """
    Open system editor to get user input and return the edited content.
    
    Args:
        initial_text: Text to pre-fill in the editor
        editor: Editor command to use. If None, uses $EDITOR environment variable or falls back to 'nano'
        suffix: File extension for the temporary file (default: '.md')
        encoding: File encoding to use (default: 'utf-8')
        delete: Whether to delete the temporary file after editing (default: True)
        dir: Directory to create the temporary file in. If None, uses system temp directory
    
    Returns:
        str: The text entered by the user in the editor
        
    Raises:
        OSError: If editor subprocess call fails
        UnicodeError: If there are encoding/decoding issues
    """
    # Resolve editor command
    editor_cmd = editor or os.environ.get('EDITOR') or 'nano'
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(
        mode='w+',
        suffix=suffix,
        encoding=encoding,
        delete=False,
        dir=dir
    ) as tf:
        # Write initial content if provided
        if initial_text:
            tf.write(initial_text)
        tf.flush()
        temp_path = Path(tf.name)
    
    try:
        # Open editor and wait for completion
        result = subprocess.run([editor_cmd, temp_path], check=True)
        if result.returncode != 0:
            raise OSError(f"Editor {editor_cmd} exited with status {result.returncode}")
        
        # Read back edited content
        with open(temp_path, 'r', encoding=encoding) as f:
            return f.read().strip()
            
    finally:
        # Clean up temp file if requested
        if delete and temp_path.exists():
            temp_path.unlink()

# Example usage:
if __name__ == "__main__":
    # Basic usage
    text = get_editor_input()
    print(f"Entered text:\n{text}")
    
    # With initial text and custom editor
    text = get_editor_input(
        initial_text="# Meeting Notes\n\n- ",
        editor="vim",
        delete=False  # Keep the temporary file
    )
    print(f"Entered text:\n{text}")
