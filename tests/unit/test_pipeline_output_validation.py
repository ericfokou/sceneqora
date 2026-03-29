from __future__ import annotations

import json
from pathlib import Path

import pytest

from sceneqora.app.validation import validate_local_pipeline_output
from sceneqora.cli import main as cli_main
from sceneqora.domain import LocalPipelineOutputValidationArtifact


def test_validate_local_pipeline_output_returns_invalid_for_missing_directory(tmp_path: Path) -> None:
    result = validate_local_pipeline_output(tmp_path / "missing")

    assert result == LocalPipelineOutputValidationArtifact(
        output_dir=str(tmp_path / "missing"),
        audio_exists=False,
        transcript_exists=False,
        segments_exists=False,
        srt_exists=False,
        segment_count=0,
        subtitle_count=0,
        status="invalid",
    )


def test_validate_local_pipeline_output_returns_invalid_for_missing_artifact(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "audio.wav").write_bytes(b"RIFF")
    (output_dir / "transcript.txt").write_text("", encoding="utf-8")
    (output_dir / "transcript_segments.json").write_text('{"segments": []}', encoding="utf-8")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.audio_exists is True
    assert result.transcript_exists is True
    assert result.segments_exists is True
    assert result.srt_exists is False


def test_validate_local_pipeline_output_rejects_empty_audio(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "audio.wav").write_bytes(b"")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.audio_exists is True


def test_validate_local_pipeline_output_rejects_invalid_json(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "transcript_segments.json").write_text("{invalid", encoding="utf-8")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.segment_count == 0


def test_validate_local_pipeline_output_rejects_json_without_segments(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "transcript_segments.json").write_text('{"status": "completed"}', encoding="utf-8")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.segment_count == 0


def test_validate_local_pipeline_output_rejects_non_empty_segments_with_empty_srt(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "transcript_segments.json").write_text(
        json.dumps(
            {
                "segments": [
                    {"start": 0.0, "end": 1.0, "text": "hello"},
                ]
            }
        ),
        encoding="utf-8",
    )
    (output_dir / "subtitles.srt").write_text("", encoding="utf-8")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"
    assert result.segment_count == 1
    assert result.subtitle_count == 0


def test_validate_local_pipeline_output_rejects_invalid_srt_syntax(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "subtitles.srt").write_text("bad srt", encoding="utf-8")

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "invalid"


def test_validate_local_pipeline_output_accepts_valid_complete_directory(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)
    (output_dir / "transcript_segments.json").write_text(
        json.dumps(
            {
                "segments": [
                    {"start": 0.0, "end": 1.0, "text": "hello"},
                    {"start": 1.5, "end": 2.0, "text": "world"},
                ]
            }
        ),
        encoding="utf-8",
    )
    (output_dir / "subtitles.srt").write_text(
        "1\n00:00:00,000 --> 00:00:01,000\nhello\n\n"
        "2\n00:00:01,500 --> 00:00:02,000\nworld\n",
        encoding="utf-8",
    )

    result = validate_local_pipeline_output(output_dir)

    assert result == LocalPipelineOutputValidationArtifact(
        output_dir=str(output_dir),
        audio_exists=True,
        transcript_exists=True,
        segments_exists=True,
        srt_exists=True,
        segment_count=2,
        subtitle_count=2,
        status="completed",
    )


def test_validate_local_pipeline_output_accepts_empty_segments_with_empty_srt(tmp_path: Path) -> None:
    output_dir = _build_valid_output_dir(tmp_path)

    result = validate_local_pipeline_output(output_dir)

    assert result.status == "completed"
    assert result.segment_count == 0
    assert result.subtitle_count == 0


def test_cli_validate_local_pipeline_output_prints_summary_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_validate(output_dir: Path) -> LocalPipelineOutputValidationArtifact:
        return LocalPipelineOutputValidationArtifact(
            output_dir=str(output_dir),
            audio_exists=True,
            transcript_exists=True,
            segments_exists=True,
            srt_exists=True,
            segment_count=0,
            subtitle_count=0,
            status="completed",
        )

    monkeypatch.setattr(cli_main, "validate_local_pipeline_output", fake_validate)

    exit_code = cli_main.main(["validate-local-pipeline-output", "/tmp/out"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "output_dir": "/tmp/out",
        "audio_exists": True,
        "transcript_exists": True,
        "segments_exists": True,
        "srt_exists": True,
        "segment_count": 0,
        "subtitle_count": 0,
        "status": "completed",
    }


def _build_valid_output_dir(tmp_path: Path) -> Path:
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "audio.wav").write_bytes(b"RIFF")
    (output_dir / "transcript.txt").write_text("", encoding="utf-8")
    (output_dir / "transcript_segments.json").write_text('{"segments": []}', encoding="utf-8")
    (output_dir / "subtitles.srt").write_text("", encoding="utf-8")
    return output_dir
