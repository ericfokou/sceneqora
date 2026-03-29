PYTHON ?= python3

.PHONY: help test lint check cli inspect inspect-video

help:
	@echo "Targets: test lint check cli inspect inspect-video"

test:
	PYTHONPATH=src $(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

check: lint test

cli:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main --help

inspect:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main inspect

inspect-video:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main inspect-video $(VIDEO)
