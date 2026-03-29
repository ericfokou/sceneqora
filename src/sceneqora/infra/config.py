"""Minimal configuration loader for Sceneqora bootstrap."""

from __future__ import annotations

from pathlib import Path

import yaml

from sceneqora.domain.models import AppConfig


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "default.yaml"


def load_app_config(config_path: Path | None = None) -> AppConfig:
    path = config_path or DEFAULT_CONFIG_PATH

    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    return AppConfig(
        profile_name=str(payload["profile_name"]),
        outputs_dir=str(payload["outputs_dir"]),
    )
