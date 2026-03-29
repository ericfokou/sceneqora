"""Minimal local audio transcription service for Sceneqora."""

from __future__ import annotations

from pathlib import Path

from sceneqora.domain import TranscriptionArtifact
from sceneqora.transcription.base import SttAdapter
from sceneqora.transcription.whisper_adapter import WhisperAdapterError, WhisperSttAdapter


class AudioTranscriptionError(RuntimeError):
    """Raised when local audio transcription fails."""


def transcribe_audio(
    source_path: str | Path,
    output_path: str | Path,
    *,
    adapter: SttAdapter | None = None,
) -> TranscriptionArtifact:
    source = Path(source_path)
    output = Path(output_path)

    _validate_source_path(source)

    stt_adapter = adapter or WhisperSttAdapter()

    try:
        transcript_text = stt_adapter.transcribe(source)
    except WhisperAdapterError as exc:
        raise AudioTranscriptionError(str(exc)) from exc
    except Exception as exc:
        raise AudioTranscriptionError(f"unexpected STT error for '{source}': {exc}") from exc

    _write_transcript(output=output, transcript_text=transcript_text)

    if not output.exists():
        raise AudioTranscriptionError(f"expected output was not created at '{output}'")

    return TranscriptionArtifact.create(
        source_path=source,
        output_path=output,
        engine=stt_adapter.engine_name,
    )


def _validate_source_path(source: Path) -> None:
    if not source.exists():
        raise AudioTranscriptionError(f"source audio was not found at '{source}'")

    if not source.is_file():
        raise AudioTranscriptionError(f"source audio is not a file: '{source}'")

    if source.suffix.lower() != ".wav":
        raise AudioTranscriptionError(f"source audio must be a .wav file: '{source}'")


def _write_transcript(*, output: Path, transcript_text: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        output.write_text(transcript_text, encoding="utf-8")
    except OSError as exc:
        raise AudioTranscriptionError(f"could not write transcript to '{output}': {exc}") from exc
