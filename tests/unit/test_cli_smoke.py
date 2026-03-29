from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from sceneqora import __version__
from sceneqora.domain import AppConfig, JobManifest, JobStatus
from sceneqora.infra import DEFAULT_CONFIG_PATH, load_app_config


ROOT = Path(__file__).resolve().parents[2]


def test_cli_help_smoke() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sceneqora.cli.main", "--help"],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Sceneqora bootstrap CLI." in result.stdout


def test_load_app_config_uses_default_yaml() -> None:
    config = load_app_config()

    assert config == AppConfig(profile_name="default", outputs_dir="outputs")


def test_default_config_yaml_matches_app_config_contract() -> None:
    payload = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))

    assert payload == {"profile_name": "default", "outputs_dir": "outputs"}


def test_job_manifest_serializes_minimal_fields() -> None:
    manifest = JobManifest.bootstrap(
        config=AppConfig(profile_name="default", outputs_dir="outputs"),
        app_version=__version__,
    )
    payload = manifest.to_dict()

    assert payload["job_id"].startswith("job-")
    assert payload["created_at"]
    assert payload["profile_name"] == "default"
    assert payload["app_version"] == __version__
    assert payload["status"] == JobStatus.BOOTSTRAPPED.value
    assert payload["config_snapshot"] == {
        "profile_name": "default",
        "outputs_dir": "outputs",
    }
    assert set(payload) == {
        "job_id",
        "created_at",
        "profile_name",
        "app_version",
        "status",
        "config_snapshot",
    }


def test_cli_inspect_prints_minimal_manifest() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sceneqora.cli.main", "inspect"],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0

    payload = yaml.safe_load(result.stdout)

    assert payload["profile_name"] == "default"
    assert payload["app_version"] == __version__
    assert payload["status"] == "bootstrapped"
    assert payload["config_snapshot"] == {
        "profile_name": "default",
        "outputs_dir": "outputs",
    }


def test_cli_help_lists_inspect_video_command() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "sceneqora.cli.main", "--help"],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "inspect-video" in result.stdout
    assert "extract-audio" in result.stdout
    assert "transcribe-audio" in result.stdout
    assert "transcribe-audio-timestamps" in result.stdout
    assert "generate-srt" in result.stdout
    assert "run-local-pipeline" in result.stdout
    assert "validate-local-pipeline-output" in result.stdout
    assert "package-run-output" in result.stdout
