.PHONY: lint clean build release test test-coverage

lint:
	ruff check .

test:
	py.test -v

test-coverage:
	pytest --cov=consilio --cov-report=term-missing --cov-report=html tests/

clean:
	rm -rf build/ dist/ *.egg-info

build: clean lint test
	python -m build

release: build
	@echo "Current version in pyproject.toml:"
	@grep "version = " pyproject.toml
	@read -p "Enter new version: " new_version; \
	sed -i '' "s/version = \".*\"/version = \"$$new_version\"/" pyproject.toml
	python -m twine upload dist/*
