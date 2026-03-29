from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

import pytest

from sceneqora.app.packaging import RunOutputPackagingError, package_run_output
from sceneqora.cli import main as cli_main
from sceneqora.domain import PackagedRunArtifact


def test_package_run_output_raises_for_missing_source_dir(tmp_path: Path) -> None:
    with pytest.raises(RunOutputPackagingError, match="source output dir was not found"):
        package_run_output(tmp_path / "missing", tmp_path / "archive.zip")


def test_package_run_output_raises_for_missing_artifact(tmp_path: Path) -> None:
    output_dir = _build_output_dir(tmp_path)
    (output_dir / "subtitles.srt").unlink()

    with pytest.raises(RunOutputPackagingError, match="missing expected artifacts: subtitles.srt"):
        package_run_output(output_dir, tmp_path / "archive.zip")


def test_package_run_output_raises_when_archive_cannot_be_created(tmp_path: Path) -> None:
    output_dir = _build_output_dir(tmp_path)
    archive_parent = tmp_path / "not-a-dir"
    archive_parent.write_text("x", encoding="utf-8")

    with pytest.raises(RunOutputPackagingError, match="archive could not be created"):
        package_run_output(output_dir, archive_parent / "archive.zip")


def test_package_run_output_overwrites_existing_archive(tmp_path: Path) -> None:
    output_dir = _build_output_dir(tmp_path)
    archive_path = tmp_path / "archive.zip"
    with ZipFile(archive_path, mode="w") as archive:
        archive.writestr("junk.txt", "junk")

    result = package_run_output(output_dir, archive_path)

    assert result.status == "completed"
    with ZipFile(archive_path, mode="r") as archive:
        assert archive.namelist() == [
            "audio.wav",
            "transcript.txt",
            "transcript_segments.json",
            "subtitles.srt",
        ]


def test_package_run_output_raises_for_incomplete_source_dir(tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "audio.wav").write_bytes(b"RIFF")

    with pytest.raises(RunOutputPackagingError, match="missing expected artifacts"):
        package_run_output(output_dir, tmp_path / "archive.zip")


def test_package_run_output_creates_valid_archive_with_exact_expected_files(tmp_path: Path) -> None:
    output_dir = _build_output_dir(tmp_path)
    archive_path = tmp_path / "archive.zip"

    result = package_run_output(output_dir, archive_path)

    assert result == PackagedRunArtifact(
        output_dir=str(output_dir),
        archive_path=str(archive_path),
        included_files=[
            "audio.wav",
            "transcript.txt",
            "transcript_segments.json",
            "subtitles.srt",
        ],
        status="completed",
    )
    with ZipFile(archive_path, mode="r") as archive:
        assert archive.namelist() == [
            "audio.wav",
            "transcript.txt",
            "transcript_segments.json",
            "subtitles.srt",
        ]


def test_cli_package_run_output_prints_summary_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_package(output_dir: Path, archive_path: Path) -> PackagedRunArtifact:
        return PackagedRunArtifact(
            output_dir=str(output_dir),
            archive_path=str(archive_path),
            included_files=[
                "audio.wav",
                "transcript.txt",
                "transcript_segments.json",
                "subtitles.srt",
            ],
            status="completed",
        )

    monkeypatch.setattr(cli_main, "package_run_output", fake_package)

    exit_code = cli_main.main(["package-run-output", "/tmp/out", "/tmp/archive.zip"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "output_dir": "/tmp/out",
        "archive_path": "/tmp/archive.zip",
        "included_files": [
            "audio.wav",
            "transcript.txt",
            "transcript_segments.json",
            "subtitles.srt",
        ],
        "status": "completed",
    }


def _build_output_dir(tmp_path: Path) -> Path:
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "audio.wav").write_bytes(b"RIFF")
    (output_dir / "transcript.txt").write_text("hello", encoding="utf-8")
    (output_dir / "transcript_segments.json").write_text('{"segments": [{"start": 0, "end": 1, "text": "hello"}]}', encoding="utf-8")
    (output_dir / "subtitles.srt").write_text(
        "1\n00:00:00,000 --> 00:00:01,000\nhello\n",
        encoding="utf-8",
    )
    return output_dir
