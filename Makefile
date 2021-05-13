.PHONY: deps

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install black flake8 flit pylint tox tox-gh-actions semantic_version polib