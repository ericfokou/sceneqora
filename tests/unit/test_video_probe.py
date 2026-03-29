from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from sceneqora.cli import main as cli_main
from sceneqora.domain import VideoAsset
from sceneqora.ingestion.probe import ProbeError, _parse_video_asset, inspect_video


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "ffprobe_video_sample.json"


def load_fixture_payload() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_parse_video_asset_returns_strict_contract() -> None:
    asset = _parse_video_asset(Path("/tmp/sample.mp4"), load_fixture_payload())

    assert asset == VideoAsset(
        source_path="/tmp/sample.mp4",
        filename="sample.mp4",
        duration_sec=12.345,
        width=1920,
        height=1080,
        fps=29.97,
        has_audio=True,
        container="mov",
    )


def test_parse_video_asset_keeps_optional_fields_as_none() -> None:
    payload = load_fixture_payload()
    payload["streams"] = [payload["streams"][0]]
    payload["format"] = {"duration": "12.345"}

    asset = _parse_video_asset(Path("/tmp/no-audio.mp4"), payload)

    assert asset.fps == 29.97
    assert asset.has_audio is False
    assert asset.container is None


def test_inspect_video_uses_ffprobe_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    completed_process = subprocess.CompletedProcess(
        args=["ffprobe"],
        returncode=0,
        stdout=FIXTURE_PATH.read_text(encoding="utf-8"),
        stderr="",
    )

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return completed_process

    monkeypatch.setattr(subprocess, "run", fake_run)

    asset = inspect_video("/tmp/sample.mp4")

    assert asset.to_dict() == {
        "source_path": "/tmp/sample.mp4",
        "filename": "sample.mp4",
        "duration_sec": 12.345,
        "width": 1920,
        "height": 1080,
        "fps": 29.97,
        "has_audio": True,
        "container": "mov",
    }


def test_inspect_video_raises_for_invalid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    completed_process = subprocess.CompletedProcess(
        args=["ffprobe"],
        returncode=0,
        stdout="not-json",
        stderr="",
    )

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return completed_process

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(ProbeError):
        inspect_video("/tmp/bad.mp4")


def test_cli_inspect_video_prints_normalized_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_inspect_video(source_path: Path) -> VideoAsset:
        return VideoAsset(
            source_path=str(source_path),
            filename=source_path.name,
            duration_sec=3.2,
            width=1280,
            height=720,
            fps=None,
            has_audio=None,
            container=None,
        )

    monkeypatch.setattr(cli_main, "inspect_video", fake_inspect_video)

    exit_code = cli_main.main(["inspect-video", "/tmp/clip.mp4"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "source_path": "/tmp/clip.mp4",
        "filename": "clip.mp4",
        "duration_sec": 3.2,
        "width": 1280,
        "height": 720,
        "fps": None,
        "has_audio": None,
        "container": None,
    }
