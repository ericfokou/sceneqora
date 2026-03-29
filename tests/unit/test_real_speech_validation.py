from __future__ import annotations

import json
from pathlib import Path

from sceneqora.app.validation import (
    validate_local_pipeline_output,
    validate_real_speech_pipeline_output,
)
from sceneqora.domain import RealSpeechPipelineOutputValidationArtifact


def test_validate_real_speech_pipeline_output_accepts_non_empty_text_artifacts(
    tmp_path: Path,
) -> None:
    output_dir = _build_voice_like_output_dir(tmp_path)

    result = validate_real_speech_pipeline_output(output_dir)

    assert result == RealSpeechPipelineOutputValidationArtifact(
        output_dir=str(output_dir),
        transcript_non_empty=True,
        segment_count=2,
        srt_non_empty=True,
        status="completed",
    )


def test_validate_real_speech_pipeline_output_rejects_empty_transcript(
    tmp_path: Path,
) -> None:
    output_dir = _build_voice_like_output_dir(tmp_path)
    (output_dir / "transcript.txt").write_text("", encoding="utf-8")

    result = validate_real_speech_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.transcript_non_empty is False
    assert result.segment_count == 2
    assert result.srt_non_empty is True


def test_validate_real_speech_pipeline_output_rejects_empty_segments(
    tmp_path: Path,
) -> None:
    output_dir = _build_voice_like_output_dir(tmp_path)
    (output_dir / "transcript_segments.json").write_text('{"segments": []}', encoding="utf-8")
    (output_dir / "subtitles.srt").write_text("", encoding="utf-8")

    result = validate_real_speech_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.transcript_non_empty is True
    assert result.segment_count == 0
    assert result.srt_non_empty is False


def test_validate_real_speech_pipeline_output_rejects_empty_srt(
    tmp_path: Path,
) -> None:
    output_dir = _build_voice_like_output_dir(tmp_path)
    (output_dir / "subtitles.srt").write_text("", encoding="utf-8")

    result = validate_real_speech_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.transcript_non_empty is True
    assert result.segment_count == 2
    assert result.srt_non_empty is False


def test_validate_real_speech_pipeline_output_can_fail_while_structural_validation_passes(
    tmp_path: Path,
) -> None:
    output_dir = _build_voice_like_output_dir(tmp_path)
    (output_dir / "transcript.txt").write_text("", encoding="utf-8")

    structural_result = validate_local_pipeline_output(output_dir)
    speech_result = validate_real_speech_pipeline_output(output_dir)

    assert structural_result.status == "completed"
    assert speech_result.status == "invalid"


def _build_voice_like_output_dir(tmp_path: Path) -> Path:
    output_dir = tmp_path / "voice-out"
    output_dir.mkdir()
    (output_dir / "audio.wav").write_bytes(b"RIFFvoice")
    (output_dir / "transcript.txt").write_text("hello from sceneqora", encoding="utf-8")
    (output_dir / "transcript_segments.json").write_text(
        json.dumps(
            {
                "segments": [
                    {"start": 0.0, "end": 0.8, "text": "hello"},
                    {"start": 0.9, "end": 1.8, "text": "from sceneqora"},
                ]
            }
        ),
        encoding="utf-8",
    )
    (output_dir / "subtitles.srt").write_text(
        "1\n00:00:00,000 --> 00:00:00,800\nhello\n\n"
        "2\n00:00:00,900 --> 00:00:01,800\nfrom sceneqora\n",
        encoding="utf-8",
    )
    return output_dir
