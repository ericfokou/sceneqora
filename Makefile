PYTHON ?= python3

.PHONY: help test lint check cli inspect inspect-video extract-audio transcribe-audio transcribe-audio-timestamps generate-srt run-local-pipeline validate-local-pipeline-output package-run-output

help:
	@echo "Targets: test lint check cli inspect inspect-video extract-audio transcribe-audio transcribe-audio-timestamps generate-srt run-local-pipeline validate-local-pipeline-output package-run-output"

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

generate-srt:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main generate-srt $(INPUT) $(OUTPUT)

run-local-pipeline:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main run-local-pipeline $(VIDEO) $(OUTPUT_DIR)

validate-local-pipeline-output:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main validate-local-pipeline-output $(OUTPUT_DIR)

package-run-output:
	PYTHONPATH=src $(PYTHON) -m sceneqora.cli.main package-run-output $(OUTPUT_DIR) $(ARCHIVE)
