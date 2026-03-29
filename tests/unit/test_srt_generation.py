from __future__ import annotations

import json
from pathlib import Path

import pytest

from sceneqora.cli import main as cli_main
from sceneqora.domain import GeneratedSrtArtifact
from sceneqora.subtitles.srt import SrtGenerationError, _format_srt_timestamp, generate_srt


def test_generate_srt_from_minimal_timestamped_json(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    output_path = tmp_path / "output.srt"
    source_path.write_text(
        json.dumps(
            {
                "segments": [
                    {"start": 0.0, "end": 1.2344, "text": "Hello"},
                    {"start": 1.2345, "end": 2.0, "text": "World"},
                ]
            }
        ),
        encoding="utf-8",
    )

    result = generate_srt(source_path, output_path)

    assert result == GeneratedSrtArtifact(
        source_path=str(source_path),
        output_path=str(output_path),
        format="srt",
        status="completed",
        subtitle_count=2,
    )
    assert output_path.read_text(encoding="utf-8") == (
        "1\n"
        "00:00:00,000 --> 00:00:01,234\n"
        "Hello\n\n"
        "2\n"
        "00:00:01,234 --> 00:00:02,000\n"
        "World\n\n"
    )


def test_srt_timestamp_conversion_uses_rounding() -> None:
    assert _format_srt_timestamp(1.2344) == "00:00:01,234"
    assert _format_srt_timestamp(1.2345) == "00:00:01,234"
    assert _format_srt_timestamp(1.2346) == "00:00:01,235"


def test_generate_srt_raises_for_missing_source(tmp_path: Path) -> None:
    with pytest.raises(SrtGenerationError, match="source transcript JSON was not found"):
        generate_srt(tmp_path / "missing.json", tmp_path / "out.srt")


def test_generate_srt_raises_for_invalid_json(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    source_path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(SrtGenerationError, match="invalid JSON"):
        generate_srt(source_path, tmp_path / "out.srt")


def test_generate_srt_raises_for_invalid_structure(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    source_path.write_text(json.dumps({"foo": []}), encoding="utf-8")

    with pytest.raises(SrtGenerationError, match="missing or invalid 'segments'"):
        generate_srt(source_path, tmp_path / "out.srt")


def test_generate_srt_raises_for_invalid_segment(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    source_path.write_text(json.dumps({"segments": [{"start": 0.0, "end": 1.0}]}), encoding="utf-8")

    with pytest.raises(SrtGenerationError, match="invalid segment payload"):
        generate_srt(source_path, tmp_path / "out.srt")


def test_generate_srt_raises_when_end_is_before_start(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    source_path.write_text(
        json.dumps({"segments": [{"start": 2.0, "end": 1.0, "text": "bad"}]}),
        encoding="utf-8",
    )

    with pytest.raises(SrtGenerationError, match="end before start"):
        generate_srt(source_path, tmp_path / "out.srt")


def test_generate_srt_writes_empty_file_when_segments_are_empty(tmp_path: Path) -> None:
    source_path = tmp_path / "segments.json"
    output_path = tmp_path / "output.srt"
    source_path.write_text(json.dumps({"segments": []}), encoding="utf-8")

    result = generate_srt(source_path, output_path)

    assert result.status == "no_subtitles"
    assert result.subtitle_count == 0
    assert output_path.read_text(encoding="utf-8") == ""


def test_generate_srt_raises_when_output_is_not_produced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "segments.json"
    output_path = tmp_path / "missing" / "output.srt"
    source_path.write_text(json.dumps({"segments": []}), encoding="utf-8")

    def fake_write_srt(*, output: Path, content: str) -> None:
        return None

    monkeypatch.setattr("sceneqora.subtitles.srt._write_srt", fake_write_srt)

    with pytest.raises(SrtGenerationError, match="expected output was not created"):
        generate_srt(source_path, output_path)


def test_cli_generate_srt_prints_confirmation_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_generate_srt(source_path: Path, output_path: Path) -> GeneratedSrtArtifact:
        return GeneratedSrtArtifact(
            source_path=str(source_path),
            output_path=str(output_path),
            format="srt",
            status="completed",
            subtitle_count=2,
        )

    monkeypatch.setattr(cli_main, "generate_srt", fake_generate_srt)

    exit_code = cli_main.main(["generate-srt", "/tmp/input.json", "/tmp/output.srt"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/input.json",
        "output_path": "/tmp/output.srt",
        "format": "srt",
        "status": "completed",
        "subtitle_count": 2,
    }
