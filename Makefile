.PHONY: dev test test-coverage type-coverage

dev:
	uv run ruff check . --fix --unsafe-fixes
	uv run ruff format .
	uv run ty check .

test:
	pytest --lf

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term --duration=5 

type-coverage:
	@echo "🔍 Checking type annotation coverage..."
	@echo "📊 Checking for missing return type annotations..."
	@uv run ruff check . --select ANN201 --quiet || echo "❌ Missing return type annotations found"
	@echo "📊 Checking for missing parameter type annotations..."
	@uv run ruff check . --select ANN001,ANN002,ANN003 --quiet || echo "❌ Missing parameter type annotations found"
	@echo "📊 Running comprehensive type check..."
	@uv run ty check . > /dev/null 2>&1 && echo "✅ Type checking passed - excellent coverage!" || echo "❌ Type checking failed"
	@echo "📊 Checking for Any usage (should be minimal)..."
	@uv run ruff check . --select ANN401 --quiet && echo "✅ No problematic Any usage found" || echo "⚠️  Some Any usage found (may be acceptable in tests)"
	@echo "📈 Type coverage assessment complete!"
