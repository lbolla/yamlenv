.PHONY: develop

develop:
	@pip install -qe .

test: tox mypy flake8

tox: requirements_tests
	tox

mypy: requirements_tests
	mypy yamlenv

flake8: requirements_tests
	flake8 yamlenv

requirements_tests: develop
	@pip install -qUr requirements_tests.txt
