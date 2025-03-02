# CONSILIO - CLAUDE ASSISTANT GUIDE

## Build & Test Commands
- `make lint` - Run ruff, mypy, and pyright for code quality checks
- `make test` - Run all tests with pytest
- `pytest tests/test_file.py::test_function` - Run a single test
- `make test-coverage` - Run tests with coverage report
- `make build` - Clean and build the project
- `make clean` - Remove build artifacts

## Code Style Guidelines
- **Type Hints**: Required for all functions. Maintain .stubs/*.pyi files if needed
- **Formatting**: Two empty lines between functions/classes, one between concept blocks
- **Imports**: Group standard lib, third-party, and project imports with blank lines
- **Functions**: Prefer top-level functions first, avoid classes unless necessary
- **Documentation**: Self-documenting code preferred over docstrings
- **Error Handling**: Fail fast with asserts, avoid try/except when possible
- **Logging**: Use `print(f"[LEVEL] {message}")` for key actions and state transitions
- **Naming**: Choose descriptive names, don't include type info in variable names
- **Code Organization**: Keep code compact, use list comprehensions when appropriate

Follow the "one man's army" philosophy - optimize for readability after a long hiatus.