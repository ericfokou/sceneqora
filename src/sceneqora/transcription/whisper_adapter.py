"""Minimal local Whisper adapter for Sceneqora audio transcription."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any


class WhisperAdapterError(RuntimeError):
    """Raised when the local Whisper adapter cannot transcribe audio."""


class WhisperSttAdapter:
    """Tiny wrapper around the local Whisper Python package."""

    engine_name = "whisper"

    def __init__(self, model_name: str = "tiny.en") -> None:
        self._model_name = model_name

    def transcribe(self, source_path: Path) -> str:
        whisper = self._import_whisper()

        try:
            model = whisper.load_model(self._model_name)
            payload = model.transcribe(str(source_path), fp16=False, verbose=False, task="transcribe")
        except Exception as exc:  # pragma: no cover - wrapped for stable CLI errors
            raise WhisperAdapterError(
                f"whisper failed for '{source_path}': {exc}"
            ) from exc

        text = payload.get("text") if isinstance(payload, dict) else None
        if not isinstance(text, str):
            raise WhisperAdapterError(f"whisper returned an invalid transcript for '{source_path}'")

        return text.strip()

    def _import_whisper(self) -> Any:
        try:
            whisper = importlib.import_module("whisper")
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise WhisperAdapterError("whisper is not available on this machine") from exc

        return whisper
