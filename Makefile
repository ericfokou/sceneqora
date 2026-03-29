PYTHON ?= python3

.PHONY: help test lint check cli inspect

help:
	@echo "Targets: test lint check cli inspect"

test:
	PYTHONPATH=src $(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

check: lint test

cli:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main --help

inspect:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main inspect
