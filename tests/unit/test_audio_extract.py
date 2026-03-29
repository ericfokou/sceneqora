from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from sceneqora.cli import main as cli_main
from sceneqora.domain import ExtractedAudio
from sceneqora.ingestion.audio import AudioExtractionError, extract_audio


def test_extract_audio_returns_minimal_contract(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "sample.wav"
    completed_process = subprocess.CompletedProcess(
        args=["ffmpeg"],
        returncode=0,
        stdout="",
        stderr="",
    )

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        output_path.write_bytes(b"RIFF")
        return completed_process

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = extract_audio("/tmp/sample.mp4", output_path)

    assert result == ExtractedAudio(
        source_path="/tmp/sample.mp4",
        output_path=str(output_path),
        sample_rate=16000,
        channels=1,
        format="wav",
    )


def test_extract_audio_raises_when_ffmpeg_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(AudioExtractionError, match="ffmpeg is not available"):
        extract_audio("/tmp/sample.mp4", "/tmp/sample.wav")


def test_extract_audio_raises_when_output_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    completed_process = subprocess.CompletedProcess(
        args=["ffmpeg"],
        returncode=0,
        stdout="",
        stderr="",
    )

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return completed_process

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(AudioExtractionError, match="expected output was not created"):
        extract_audio("/tmp/sample.mp4", tmp_path / "missing.wav")


def test_cli_extract_audio_prints_confirmation_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_extract_audio(source_path: Path, output_path: Path) -> ExtractedAudio:
        return ExtractedAudio(
            source_path=str(source_path),
            output_path=str(output_path),
            sample_rate=16000,
            channels=1,
            format="wav",
        )

    monkeypatch.setattr(cli_main, "extract_audio", fake_extract_audio)

    exit_code = cli_main.main(["extract-audio", "/tmp/clip.mp4", "/tmp/clip.wav"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/clip.mp4",
        "output_path": "/tmp/clip.wav",
        "sample_rate": 16000,
        "channels": 1,
        "format": "wav",
    }
