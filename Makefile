.PHONY: deps cenv env lint tox publish

deps:  ## Install dependencies
	python -m pip install --upgrade pip
	python -m pip install black flake8 flit pylint tox tox-gh-actions semantic_version polib

cenv:  ## Create the virtual-environment
	python3 -m venv env

env:
	@echo "For entering the virtual-environment just type:"
	@echo ". env/bin/activate"

lint:  ## Lint and static-check
	python -m flake8 icm
	python -m pylint icm

tox:   ## Run tox
	python -m tox

publish:  ## Publish to PyPi
	python -m flit publish

install:  ## Install the tool locally
	flit build
	flit install