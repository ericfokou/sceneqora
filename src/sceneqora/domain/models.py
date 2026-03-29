"""Core domain models for the Sceneqora bootstrap pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path


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


@dataclass(frozen=True, slots=True)
class VideoAsset:
    """Minimal normalized metadata for a probed input video."""

    source_path: str
    filename: str
    duration_sec: float
    width: int
    height: int
    fps: float | None
    has_audio: bool | None
    container: str | None

    @classmethod
    def create(
        cls,
        source_path: Path,
        duration_sec: float,
        width: int,
        height: int,
        fps: float | None,
        has_audio: bool | None,
        container: str | None,
    ) -> "VideoAsset":
        return cls(
            source_path=str(source_path),
            filename=source_path.name,
            duration_sec=duration_sec,
            width=width,
            height=height,
            fps=fps,
            has_audio=has_audio,
            container=container,
        )

    def to_dict(self) -> dict[str, str | int | float | bool | None]:
        return asdict(self)
