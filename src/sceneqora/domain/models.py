"""Core domain models for the Sceneqora bootstrap pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum


class JobStatus(StrEnum):
    """Minimal lifecycle states for a bootstrap job."""

    BOOTSTRAPPED = "bootstrapped"


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Minimal application configuration loaded from configs/default.yaml."""

    profile_name: str
    outputs_dir: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
