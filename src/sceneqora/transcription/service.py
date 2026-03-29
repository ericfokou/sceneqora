"""Minimal local audio transcription service for Sceneqora."""

from __future__ import annotations

import json
from pathlib import Path

from sceneqora.domain import (
    TimestampedTranscriptSegment,
    TimestampedTranscriptionArtifact,
    TranscriptionArtifact,
)
from sceneqora.transcription.base import SttAdapter, TimestampedSttAdapter
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


def transcribe_audio_timestamps(
    source_path: str | Path,
    output_path: str | Path,
    *,
    adapter: TimestampedSttAdapter | None = None,
) -> TimestampedTranscriptionArtifact:
    source = Path(source_path)
    output = Path(output_path)

    _validate_source_path(source)

    stt_adapter = adapter or WhisperSttAdapter()

    try:
        raw_segments = stt_adapter.transcribe_segments(source)
    except WhisperAdapterError as exc:
        raise AudioTranscriptionError(str(exc)) from exc
    except Exception as exc:
        raise AudioTranscriptionError(f"unexpected STT error for '{source}': {exc}") from exc

    segments = _normalize_segments(source=source, raw_segments=raw_segments)
    artifact = TimestampedTranscriptionArtifact.create(
        source_path=source,
        output_path=output,
        engine=stt_adapter.engine_name,
        segments=segments,
    )
    _write_timestamped_transcript(output=output, artifact=artifact)

    if not output.exists():
        raise AudioTranscriptionError(f"expected output was not created at '{output}'")

    return artifact


def _normalize_segments(
    *,
    source: Path,
    raw_segments: list[dict[str, float | str]],
) -> list[TimestampedTranscriptSegment]:
    segments: list[TimestampedTranscriptSegment] = []
    for raw_segment in raw_segments:
        try:
            start = float(raw_segment["start"])
            end = float(raw_segment["end"])
            text = str(raw_segment["text"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AudioTranscriptionError(f"invalid segment payload for '{source}'") from exc

        segments.append(TimestampedTranscriptSegment(start=start, end=end, text=text))

    return segments


def _write_timestamped_transcript(
    *,
    output: Path,
    artifact: TimestampedTranscriptionArtifact,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        output.write_text(
            json.dumps(artifact.to_dict(), indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise AudioTranscriptionError(f"could not write transcript JSON to '{output}': {exc}") from exc
