.PHONY: develop bump2version clean-repo

# Self-documenting Makefile
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:  ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

develop:  ## Install package for development
	@pip install -qe .

test: tox mypy flake8  ## Run all tests

tox: requirements_tests  ## Run unittests
	tox

mypy: requirements_tests  ## Run mypy linter
	mypy yamlenv

flake8: requirements_tests  ## Run flake8 linter
	flake8 yamlenv

requirements_tests: develop  ## Install requirements for tests
	@pip install -qUr requirements_tests.txt

clean-repo:  ## Check repository is clean
	git diff --quiet HEAD  # pending commits
	git diff --cached --quiet HEAD  # unstaged changes
	git pull --ff-only  # latest code

bump2version:
	pip install -U bump2version

release: bump2version clean-repo  ## Make a release (specify: PART=[major|minor|patch])
	bump2version ${PART}
	git push
	git push --tags
