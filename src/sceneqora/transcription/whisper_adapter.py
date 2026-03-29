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

    def transcribe_segments(self, source_path: Path) -> list[dict[str, float | str]]:
        whisper = self._import_whisper()

        try:
            model = whisper.load_model(self._model_name)
            payload = model.transcribe(str(source_path), fp16=False, verbose=False, task="transcribe")
        except Exception as exc:  # pragma: no cover - wrapped for stable CLI errors
            raise WhisperAdapterError(
                f"whisper failed for '{source_path}': {exc}"
            ) from exc

        raw_segments = payload.get("segments") if isinstance(payload, dict) else None
        if raw_segments is None:
            return []
        if not isinstance(raw_segments, list):
            raise WhisperAdapterError(f"whisper returned invalid segments for '{source_path}'")

        segments: list[dict[str, float | str]] = []
        for raw_segment in raw_segments:
            if not isinstance(raw_segment, dict):
                raise WhisperAdapterError(f"whisper returned invalid segments for '{source_path}'")

            try:
                start = float(raw_segment["start"])
                end = float(raw_segment["end"])
                text = str(raw_segment["text"]).strip()
            except (KeyError, TypeError, ValueError) as exc:
                raise WhisperAdapterError(
                    f"whisper returned invalid segments for '{source_path}'"
                ) from exc

            segments.append({"start": start, "end": end, "text": text})

        return segments

    def _import_whisper(self) -> Any:
        try:
            whisper = importlib.import_module("whisper")
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise WhisperAdapterError("whisper is not available on this machine") from exc

        return whisper
