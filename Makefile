.PHONY: lint clean build release

lint:
	ruff check .

test:
	py.test -v

clean:
	rm -rf build/ dist/ *.egg-info

build: clean
	python -m build

release: build
	@echo "Current version in pyproject.toml:"
	@grep "version = " pyproject.toml
	@read -p "Enter new version: " new_version; \
	sed -i '' "s/version = \".*\"/version = \"$$new_version\"/" pyproject.toml
	python -m twine upload dist/*
