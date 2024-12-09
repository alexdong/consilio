.PHONY: lint clean build release test test-coverage

lint:
	ruff check .

test: lint
	py.test -v

test-coverage: test
	pytest --cov=consilio --cov-report=term-missing --cov-report=html tests/

clean:
	rm -rf build/ dist/ *.egg-info

build: clean
	python -m build

release: build
	$(eval VERSION := $(shell grep '^version = ' pyproject.toml | sed -E 's/version = "(.*)"/\1/'))                                                                                   
	@echo "Releasing version $(VERSION)"                                                                                                                                              
	git tag -a "v$(VERSION)" -m "Release version $(VERSION)"                                                                                                                          
	git push origin "v$(VERSION)"                                                                                                                                                     
	gh release create "v$(VERSION)" --title "Release v$(VERSION)" --notes "Release version $(VERSION)"