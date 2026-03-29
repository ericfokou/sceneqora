"""Minimal STT adapter contract for Sceneqora."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class SttAdapter(Protocol):
    """Minimal interface for local speech-to-text adapters."""

    engine_name: str

    def transcribe(self, source_path: Path) -> str:
        """Return plain transcript text for a local audio file."""
