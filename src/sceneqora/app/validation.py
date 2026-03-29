"""Minimal validation for local pipeline outputs."""

from __future__ import annotations

import json
import re
from pathlib import Path

from sceneqora.domain import (
    LocalPipelineOutputValidationArtifact,
    RealSpeechPipelineOutputValidationArtifact,
)


_TIMESTAMP_PATTERN = re.compile(
    r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$"
)


def validate_local_pipeline_output(output_dir: Path) -> LocalPipelineOutputValidationArtifact:
    """Validate the minimal structure and coherence of one local pipeline output."""

    audio_path = output_dir / "audio.wav"
    transcript_path = output_dir / "transcript.txt"
    segments_path = output_dir / "transcript_segments.json"
    srt_path = output_dir / "subtitles.srt"

    audio_exists = output_dir.is_dir() and audio_path.is_file()
    transcript_exists = output_dir.is_dir() and transcript_path.is_file()
    segments_exists = output_dir.is_dir() and segments_path.is_file()
    srt_exists = output_dir.is_dir() and srt_path.is_file()

    if not output_dir.exists() or not output_dir.is_dir():
        return _build_result(
            output_dir=output_dir,
            audio_exists=False,
            transcript_exists=False,
            segments_exists=False,
            srt_exists=False,
            segment_count=0,
            subtitle_count=0,
            status="invalid",
        )

    if not all((audio_exists, transcript_exists, segments_exists, srt_exists)):
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=0,
            subtitle_count=0,
            status="invalid",
        )

    if audio_path.stat().st_size == 0:
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=0,
            subtitle_count=0,
            status="invalid",
        )

    try:
        payload = json.loads(segments_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=0,
            subtitle_count=0,
            status="invalid",
        )

    segments = payload.get("segments")
    if not isinstance(segments, list):
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=0,
            subtitle_count=0,
            status="invalid",
        )

    try:
        subtitle_count = _count_srt_blocks(srt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=len(segments),
            subtitle_count=0,
            status="invalid",
        )

    segment_count = len(segments)
    if segment_count > 0 and subtitle_count == 0:
        return _build_result(
            output_dir=output_dir,
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=segment_count,
            subtitle_count=subtitle_count,
            status="invalid",
        )

    return _build_result(
        output_dir=output_dir,
        audio_exists=audio_exists,
        transcript_exists=transcript_exists,
        segments_exists=segments_exists,
        srt_exists=srt_exists,
        segment_count=segment_count,
        subtitle_count=subtitle_count,
        status="completed",
    )


def validate_real_speech_pipeline_output(output_dir: Path) -> RealSpeechPipelineOutputValidationArtifact:
    """Validate that one local pipeline output contains non-empty speech artifacts."""

    structural_result = validate_local_pipeline_output(output_dir)
    transcript_path = output_dir / "transcript.txt"
    segments_path = output_dir / "transcript_segments.json"
    srt_path = output_dir / "subtitles.srt"

    transcript_non_empty = transcript_path.is_file() and bool(
        transcript_path.read_text(encoding="utf-8").strip()
    )
    srt_non_empty = srt_path.is_file() and bool(srt_path.read_text(encoding="utf-8").strip())

    segment_count = 0
    if segments_path.is_file():
        try:
            payload = json.loads(segments_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            segment_count = 0
        else:
            segments = payload.get("segments")
            if isinstance(segments, list):
                segment_count = len(segments)

    status = "completed"
    if structural_result.status != "completed":
        status = "invalid"
    elif not transcript_non_empty or segment_count == 0 or not srt_non_empty:
        status = "invalid"

    return RealSpeechPipelineOutputValidationArtifact.create(
        output_dir=output_dir,
        transcript_non_empty=transcript_non_empty,
        segment_count=segment_count,
        srt_non_empty=srt_non_empty,
        status=status,
    )


def _build_result(
    *,
    output_dir: Path,
    audio_exists: bool,
    transcript_exists: bool,
    segments_exists: bool,
    srt_exists: bool,
    segment_count: int,
    subtitle_count: int,
    status: str,
) -> LocalPipelineOutputValidationArtifact:
    return LocalPipelineOutputValidationArtifact.create(
        output_dir=output_dir,
        audio_exists=audio_exists,
        transcript_exists=transcript_exists,
        segments_exists=segments_exists,
        srt_exists=srt_exists,
        segment_count=segment_count,
        subtitle_count=subtitle_count,
        status=status,
    )


def _count_srt_blocks(content: str) -> int:
    stripped = content.strip()
    if not stripped:
        return 0

    blocks = re.split(r"\n\s*\n", stripped)
    count = 0
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError("SRT block is incomplete")
        if not lines[0].isdigit():
            raise ValueError("SRT block index is invalid")
        if not _TIMESTAMP_PATTERN.match(lines[1]):
            raise ValueError("SRT timestamp line is invalid")
        count += 1
    return count
