"""Minimal ffmpeg-based local audio extraction for Sceneqora."""

from __future__ import annotations

import subprocess
from pathlib import Path

from sceneqora.domain import ExtractedAudio


class AudioExtractionError(RuntimeError):
    """Raised when local audio extraction fails."""


def extract_audio(source_path: str | Path, output_path: str | Path) -> ExtractedAudio:
    source = Path(source_path)
    output = Path(output_path)
    _run_ffmpeg_extract(source=source, output=output)
    return ExtractedAudio.create(source_path=source, output_path=output)


def _run_ffmpeg_extract(*, source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise AudioExtractionError("ffmpeg is not available on this machine") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip() or "ffmpeg failed"
        raise AudioExtractionError(f"ffmpeg error for '{source}': {stderr}")

    if not output.exists():
        raise AudioExtractionError(f"expected output was not created at '{output}'")
