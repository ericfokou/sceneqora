"""Minimal sequential local pipeline assembly for Sceneqora."""

from __future__ import annotations

from pathlib import Path

from sceneqora.domain import LocalPipelineRunArtifact
from sceneqora.ingestion import extract_audio
from sceneqora.subtitles import generate_srt
from sceneqora.transcription import transcribe_audio, transcribe_audio_timestamps


class LocalPipelineRunError(RuntimeError):
    """Raised when the minimal local pipeline fails."""


def run_local_pipeline(source_path: str | Path, output_dir: str | Path) -> LocalPipelineRunArtifact:
    source = Path(source_path)
    output = Path(output_dir)

    _validate_source_path(source)
    _prepare_output_dir(output)

    audio_path = output / "audio.wav"
    transcript_path = output / "transcript.txt"
    segments_path = output / "transcript_segments.json"
    srt_path = output / "subtitles.srt"

    try:
        extract_audio(source, audio_path)
        _require_artifact(audio_path, stage_name="audio extraction")

        transcribe_audio(audio_path, transcript_path)
        _require_artifact(transcript_path, stage_name="text transcription")

        transcribe_audio_timestamps(audio_path, segments_path)
        _require_artifact(segments_path, stage_name="timestamped transcription")

        generate_srt(segments_path, srt_path)
        _require_artifact(srt_path, stage_name="SRT generation")
    except Exception as exc:
        raise LocalPipelineRunError(f"pipeline failed for '{source}': {exc}") from exc

    return LocalPipelineRunArtifact.create(
        source_path=source,
        output_dir=output,
        audio_path=audio_path,
        transcript_path=transcript_path,
        segments_path=segments_path,
        srt_path=srt_path,
    )


def _validate_source_path(source: Path) -> None:
    if not source.exists():
        raise LocalPipelineRunError(f"source video was not found at '{source}'")

    if not source.is_file():
        raise LocalPipelineRunError(f"source video is not a file: '{source}'")


def _prepare_output_dir(output_dir: Path) -> None:
    if output_dir.exists() and not output_dir.is_dir():
        raise LocalPipelineRunError(f"output dir is not a directory: '{output_dir}'")

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise LocalPipelineRunError(f"could not create output dir '{output_dir}': {exc}") from exc


def _require_artifact(path: Path, *, stage_name: str) -> None:
    if not path.exists():
        raise LocalPipelineRunError(f"{stage_name} did not produce expected artifact '{path}'")
