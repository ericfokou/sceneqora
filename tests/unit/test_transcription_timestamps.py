from __future__ import annotations

import json
from pathlib import Path

import pytest

from sceneqora.cli import main as cli_main
from sceneqora.domain import TimestampedTranscriptSegment, TimestampedTranscriptionArtifact
from sceneqora.transcription import transcribe_audio_timestamps
from sceneqora.transcription.service import AudioTranscriptionError
from sceneqora.transcription.whisper_adapter import WhisperAdapterError


class DummyTimestampAdapter:
    engine_name = "dummy-stt"

    def __init__(self, segments: list[dict[str, float | str]]) -> None:
        self._segments = segments

    def transcribe_segments(self, source_path: Path) -> list[dict[str, float | str]]:
        return self._segments


class FailingTimestampAdapter:
    engine_name = "dummy-stt"

    def transcribe_segments(self, source_path: Path) -> list[dict[str, float | str]]:
        raise WhisperAdapterError("dummy timestamp STT failure")


def test_transcribe_audio_timestamps_returns_minimal_json_contract(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.wav"
    output_path = tmp_path / "sample.json"
    source_path.write_bytes(b"RIFF")

    result = transcribe_audio_timestamps(
        source_path,
        output_path,
        adapter=DummyTimestampAdapter(
            [
                {"start": 0.0, "end": 0.5, "text": "hello"},
                {"start": 0.5, "end": 1.0, "text": "world"},
            ]
        ),
    )

    assert result == TimestampedTranscriptionArtifact(
        source_path=str(source_path),
        output_path=str(output_path),
        format="json",
        engine="dummy-stt",
        status="completed",
        segments=[
            TimestampedTranscriptSegment(start=0.0, end=0.5, text="hello"),
            TimestampedTranscriptSegment(start=0.5, end=1.0, text="world"),
        ],
    )
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload == {
        "source_path": str(source_path),
        "output_path": str(output_path),
        "format": "json",
        "engine": "dummy-stt",
        "status": "completed",
        "segments": [
            {"start": 0.0, "end": 0.5, "text": "hello"},
            {"start": 0.5, "end": 1.0, "text": "world"},
        ],
    }


def test_transcribe_audio_timestamps_returns_empty_segments_json(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.wav"
    output_path = tmp_path / "sample.json"
    source_path.write_bytes(b"RIFF")

    result = transcribe_audio_timestamps(
        source_path,
        output_path,
        adapter=DummyTimestampAdapter([]),
    )

    assert result.status == "no_segments"
    assert result.segments == []
    assert result.to_cli_dict()["segment_count"] == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["status"] == "no_segments"
    assert payload["segments"] == []


def test_transcribe_audio_timestamps_raises_for_missing_source(tmp_path: Path) -> None:
    with pytest.raises(AudioTranscriptionError, match="source audio was not found"):
        transcribe_audio_timestamps(
            tmp_path / "missing.wav",
            tmp_path / "out.json",
            adapter=DummyTimestampAdapter([]),
        )


def test_transcribe_audio_timestamps_raises_for_engine_failure(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.wav"
    source_path.write_bytes(b"RIFF")

    with pytest.raises(AudioTranscriptionError, match="dummy timestamp STT failure"):
        transcribe_audio_timestamps(source_path, tmp_path / "out.json", adapter=FailingTimestampAdapter())


def test_transcribe_audio_timestamps_raises_when_output_is_not_produced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.wav"
    output_path = tmp_path / "missing/out.json"
    source_path.write_bytes(b"RIFF")

    def fake_write_timestamped_transcript(
        *,
        output: Path,
        artifact: TimestampedTranscriptionArtifact,
    ) -> None:
        return None

    monkeypatch.setattr(
        "sceneqora.transcription.service._write_timestamped_transcript",
        fake_write_timestamped_transcript,
    )

    with pytest.raises(AudioTranscriptionError, match="expected output was not created"):
        transcribe_audio_timestamps(
            source_path,
            output_path,
            adapter=DummyTimestampAdapter([]),
        )


def test_cli_transcribe_audio_timestamps_prints_confirmation_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_transcribe_audio_timestamps(
        source_path: Path,
        output_path: Path,
    ) -> TimestampedTranscriptionArtifact:
        return TimestampedTranscriptionArtifact(
            source_path=str(source_path),
            output_path=str(output_path),
            format="json",
            engine="whisper",
            status="completed",
            segments=[TimestampedTranscriptSegment(start=0.0, end=0.5, text="hello")],
        )

    monkeypatch.setattr(cli_main, "transcribe_audio_timestamps", fake_transcribe_audio_timestamps)

    exit_code = cli_main.main(
        ["transcribe-audio-timestamps", "/tmp/audio.wav", "/tmp/audio_segments.json"]
    )
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/audio.wav",
        "output_path": "/tmp/audio_segments.json",
        "format": "json",
        "engine": "whisper",
        "status": "completed",
        "segment_count": 1,
    }
