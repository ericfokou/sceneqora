from __future__ import annotations

import json
from pathlib import Path

import pytest

from sceneqora.cli import main as cli_main
from sceneqora.domain import TranscriptionArtifact
from sceneqora.transcription import transcribe_audio
from sceneqora.transcription.service import AudioTranscriptionError
from sceneqora.transcription.whisper_adapter import WhisperAdapterError


class DummyAdapter:
    engine_name = "dummy-stt"

    def __init__(self, text: str = "hello world") -> None:
        self._text = text

    def transcribe(self, source_path: Path) -> str:
        return self._text


class FailingAdapter:
    engine_name = "dummy-stt"

    def transcribe(self, source_path: Path) -> str:
        raise WhisperAdapterError("dummy STT failure")


def test_transcribe_audio_returns_minimal_contract(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.wav"
    output_path = tmp_path / "sample.txt"
    source_path.write_bytes(b"RIFF")

    result = transcribe_audio(source_path, output_path, adapter=DummyAdapter("sceneqora test"))

    assert result == TranscriptionArtifact(
        source_path=str(source_path),
        output_path=str(output_path),
        format="txt",
        engine="dummy-stt",
        status="completed",
    )
    assert output_path.read_text(encoding="utf-8") == "sceneqora test"


def test_transcribe_audio_raises_for_missing_source(tmp_path: Path) -> None:
    with pytest.raises(AudioTranscriptionError, match="source audio was not found"):
        transcribe_audio(tmp_path / "missing.wav", tmp_path / "out.txt", adapter=DummyAdapter())


def test_transcribe_audio_raises_for_engine_failure(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.wav"
    source_path.write_bytes(b"RIFF")

    with pytest.raises(AudioTranscriptionError, match="dummy STT failure"):
        transcribe_audio(source_path, tmp_path / "out.txt", adapter=FailingAdapter())


def test_transcribe_audio_raises_when_output_is_not_produced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.wav"
    output_path = tmp_path / "missing/out.txt"
    source_path.write_bytes(b"RIFF")

    def fake_write_transcript(*, output: Path, transcript_text: str) -> None:
        return None

    monkeypatch.setattr("sceneqora.transcription.service._write_transcript", fake_write_transcript)

    with pytest.raises(AudioTranscriptionError, match="expected output was not created"):
        transcribe_audio(source_path, output_path, adapter=DummyAdapter())


def test_cli_transcribe_audio_prints_confirmation_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_transcribe_audio(source_path: Path, output_path: Path) -> TranscriptionArtifact:
        return TranscriptionArtifact(
            source_path=str(source_path),
            output_path=str(output_path),
            format="txt",
            engine="whisper",
            status="completed",
        )

    monkeypatch.setattr(cli_main, "transcribe_audio", fake_transcribe_audio)

    exit_code = cli_main.main(["transcribe-audio", "/tmp/audio.wav", "/tmp/audio.txt"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/audio.wav",
        "output_path": "/tmp/audio.txt",
        "format": "txt",
        "engine": "whisper",
        "status": "completed",
    }
