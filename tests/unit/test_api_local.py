from __future__ import annotations

from importlib import import_module
from pathlib import Path

from fastapi.testclient import TestClient

from sceneqora.app import LocalPipelineRunError
from sceneqora.domain import LocalPipelineRunArtifact


api_module = import_module("sceneqora.api.app")
client = TestClient(api_module.app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_runs_returns_success_payload(monkeypatch, tmp_path: Path) -> None:
    source_path = tmp_path / "video.mp4"
    source_path.write_bytes(b"video")

    def fake_run_local_pipeline(source_path: str, output_dir: str) -> LocalPipelineRunArtifact:
        output = Path(output_dir)
        return LocalPipelineRunArtifact(
            source_path=source_path,
            output_dir=output_dir,
            audio_path=str(output / "audio.wav"),
            transcript_path=str(output / "transcript.txt"),
            segments_path=str(output / "transcript_segments.json"),
            srt_path=str(output / "subtitles.srt"),
            status="completed",
        )

    monkeypatch.setattr(api_module, "run_local_pipeline", fake_run_local_pipeline)

    response = client.post(
        "/runs",
        json={"source_path": str(source_path), "output_dir": str(tmp_path / "out")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "source_path": str(source_path),
        "output_dir": str(tmp_path / "out"),
        "audio_path": str(tmp_path / "out" / "audio.wav"),
        "transcript_path": str(tmp_path / "out" / "transcript.txt"),
        "segments_path": str(tmp_path / "out" / "transcript_segments.json"),
        "srt_path": str(tmp_path / "out" / "subtitles.srt"),
        "status": "completed",
    }


def test_post_runs_returns_400_for_absent_payload() -> None:
    response = client.post("/runs")

    assert response.status_code == 400
    assert response.json()["detail"] == "invalid request payload"


def test_post_runs_returns_400_for_invalid_payload() -> None:
    response = client.post("/runs", json={"source_path": 123, "output_dir": []})

    assert response.status_code == 400
    assert response.json()["detail"] == "invalid request payload"


def test_post_runs_returns_400_for_missing_source_path() -> None:
    response = client.post("/runs", json={"output_dir": "/tmp/out"})

    assert response.status_code == 400
    assert response.json()["detail"] == "invalid request payload"


def test_post_runs_returns_400_for_missing_output_dir(tmp_path: Path) -> None:
    source_path = tmp_path / "video.mp4"
    source_path.write_bytes(b"video")

    response = client.post("/runs", json={"source_path": str(source_path)})

    assert response.status_code == 400
    assert response.json()["detail"] == "invalid request payload"


def test_post_runs_returns_404_for_missing_source_file(tmp_path: Path) -> None:
    response = client.post(
        "/runs",
        json={"source_path": str(tmp_path / "missing.mp4"), "output_dir": str(tmp_path / "out")},
    )

    assert response.status_code == 404
    assert "source_path was not found" in response.json()["detail"]


def test_post_runs_returns_500_for_pipeline_failure(monkeypatch, tmp_path: Path) -> None:
    source_path = tmp_path / "video.mp4"
    source_path.write_bytes(b"video")

    def fake_run_local_pipeline(source_path: str, output_dir: str) -> LocalPipelineRunArtifact:
        raise LocalPipelineRunError(f"pipeline failed for '{source_path}'")

    monkeypatch.setattr(api_module, "run_local_pipeline", fake_run_local_pipeline)

    response = client.post(
        "/runs",
        json={"source_path": str(source_path), "output_dir": str(tmp_path / "out")},
    )

    assert response.status_code == 500
    assert "pipeline failed" in response.json()["detail"]


def test_unknown_endpoint_returns_404() -> None:
    response = client.get("/unknown")

    assert response.status_code == 404


def test_invalid_method_returns_405() -> None:
    response = client.put("/health")

    assert response.status_code == 405
