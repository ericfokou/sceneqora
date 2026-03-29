from __future__ import annotations

import json
from pathlib import Path

import pytest

from sceneqora.app.pipeline import LocalPipelineRunError, run_local_pipeline
from sceneqora.cli import main as cli_main
from sceneqora.domain import LocalPipelineRunArtifact


def test_run_local_pipeline_returns_minimal_summary(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.mp4"
    output_dir = tmp_path / "out"
    source_path.write_bytes(b"video")

    def fake_extract_audio(source: Path, output: Path) -> object:
        output.write_bytes(b"RIFF")
        return object()

    def fake_transcribe_audio(source: Path, output: Path) -> object:
        output.write_text("hello world", encoding="utf-8")
        return object()

    def fake_transcribe_audio_timestamps(source: Path, output: Path) -> object:
        output.write_text('{"segments": []}\n', encoding="utf-8")
        return object()

    def fake_generate_srt(source: Path, output: Path) -> object:
        output.write_text("", encoding="utf-8")
        return object()

    monkeypatch.setattr("sceneqora.app.pipeline.extract_audio", fake_extract_audio)
    monkeypatch.setattr("sceneqora.app.pipeline.transcribe_audio", fake_transcribe_audio)
    monkeypatch.setattr("sceneqora.app.pipeline.transcribe_audio_timestamps", fake_transcribe_audio_timestamps)
    monkeypatch.setattr("sceneqora.app.pipeline.generate_srt", fake_generate_srt)

    result = run_local_pipeline(source_path, output_dir)

    assert result == LocalPipelineRunArtifact(
        source_path=str(source_path),
        output_dir=str(output_dir),
        audio_path=str(output_dir / "audio.wav"),
        transcript_path=str(output_dir / "transcript.txt"),
        segments_path=str(output_dir / "transcript_segments.json"),
        srt_path=str(output_dir / "subtitles.srt"),
        status="completed",
    )


def test_run_local_pipeline_raises_for_missing_video(tmp_path: Path) -> None:
    with pytest.raises(LocalPipelineRunError, match="source video was not found"):
        run_local_pipeline(tmp_path / "missing.mp4", tmp_path / "out")


def test_run_local_pipeline_raises_for_invalid_output_dir(tmp_path: Path) -> None:
    source_path = tmp_path / "sample.mp4"
    output_path = tmp_path / "out"
    source_path.write_bytes(b"video")
    output_path.write_text("not a dir", encoding="utf-8")

    with pytest.raises(LocalPipelineRunError, match="output dir is not a directory"):
        run_local_pipeline(source_path, output_path)


def test_run_local_pipeline_stops_on_first_blocking_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.mp4"
    output_dir = tmp_path / "out"
    source_path.write_bytes(b"video")
    calls: list[str] = []

    def fake_extract_audio(source: Path, output: Path) -> object:
        calls.append("extract_audio")
        raise RuntimeError("boom")

    def fake_transcribe_audio(source: Path, output: Path) -> object:
        calls.append("transcribe_audio")
        return object()

    monkeypatch.setattr("sceneqora.app.pipeline.extract_audio", fake_extract_audio)
    monkeypatch.setattr("sceneqora.app.pipeline.transcribe_audio", fake_transcribe_audio)

    with pytest.raises(LocalPipelineRunError, match="pipeline failed"):
        run_local_pipeline(source_path, output_dir)

    assert calls == ["extract_audio"]


def test_run_local_pipeline_raises_when_intermediate_artifact_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.mp4"
    output_dir = tmp_path / "out"
    source_path.write_bytes(b"video")

    def fake_extract_audio(source: Path, output: Path) -> object:
        return object()

    monkeypatch.setattr("sceneqora.app.pipeline.extract_audio", fake_extract_audio)

    with pytest.raises(LocalPipelineRunError, match="audio extraction did not produce expected artifact"):
        run_local_pipeline(source_path, output_dir)


def test_run_local_pipeline_reuses_existing_output_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "sample.mp4"
    output_dir = tmp_path / "out"
    source_path.write_bytes(b"video")
    output_dir.mkdir()

    def fake_extract_audio(source: Path, output: Path) -> object:
        output.write_bytes(b"RIFF")
        return object()

    def fake_transcribe_audio(source: Path, output: Path) -> object:
        output.write_text("hello", encoding="utf-8")
        return object()

    def fake_transcribe_audio_timestamps(source: Path, output: Path) -> object:
        output.write_text('{"segments": []}\n', encoding="utf-8")
        return object()

    def fake_generate_srt(source: Path, output: Path) -> object:
        output.write_text("", encoding="utf-8")
        return object()

    monkeypatch.setattr("sceneqora.app.pipeline.extract_audio", fake_extract_audio)
    monkeypatch.setattr("sceneqora.app.pipeline.transcribe_audio", fake_transcribe_audio)
    monkeypatch.setattr("sceneqora.app.pipeline.transcribe_audio_timestamps", fake_transcribe_audio_timestamps)
    monkeypatch.setattr("sceneqora.app.pipeline.generate_srt", fake_generate_srt)

    result = run_local_pipeline(source_path, output_dir)

    assert output_dir.is_dir()
    assert result.output_dir == str(output_dir)


def test_cli_run_local_pipeline_prints_summary_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run_local_pipeline(source_path: Path, output_dir: Path) -> LocalPipelineRunArtifact:
        return LocalPipelineRunArtifact(
            source_path=str(source_path),
            output_dir=str(output_dir),
            audio_path=str(output_dir / "audio.wav"),
            transcript_path=str(output_dir / "transcript.txt"),
            segments_path=str(output_dir / "transcript_segments.json"),
            srt_path=str(output_dir / "subtitles.srt"),
            status="completed",
        )

    monkeypatch.setattr(cli_main, "run_local_pipeline", fake_run_local_pipeline)

    exit_code = cli_main.main(["run-local-pipeline", "/tmp/video.mp4", "/tmp/out"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/video.mp4",
        "output_dir": "/tmp/out",
        "audio_path": "/tmp/out/audio.wav",
        "transcript_path": "/tmp/out/transcript.txt",
        "segments_path": "/tmp/out/transcript_segments.json",
        "srt_path": "/tmp/out/subtitles.srt",
        "status": "completed",
    }
