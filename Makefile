PYTHON ?= python3

.PHONY: help test lint check cli inspect inspect-video extract-audio transcribe-audio transcribe-audio-timestamps

help:
	@echo "Targets: test lint check cli inspect inspect-video extract-audio transcribe-audio transcribe-audio-timestamps"

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

extract-audio:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main extract-audio $(VIDEO) $(OUTPUT)

transcribe-audio:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main transcribe-audio $(AUDIO) $(OUTPUT)

transcribe-audio-timestamps:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main transcribe-audio-timestamps $(AUDIO) $(OUTPUT)
