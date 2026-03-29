"""Minimal manifest contract for Sceneqora bootstrap jobs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from sceneqora.domain.models import AppConfig, JobStatus


@dataclass(frozen=True, slots=True)
class JobManifest:
    """Minimal serializable manifest for inspecting bootstrap state."""

    job_id: str
    created_at: str
    profile_name: str
    app_version: str
    status: JobStatus
    config_snapshot: dict[str, str]

    @classmethod
    def bootstrap(cls, config: AppConfig, app_version: str) -> "JobManifest":
        return cls(
            job_id=f"job-{uuid4().hex[:12]}",
            created_at=datetime.now(timezone.utc).isoformat(),
            profile_name=config.profile_name,
            app_version=app_version,
            status=JobStatus.BOOTSTRAPPED,
            config_snapshot=config.to_dict(),
        )

    def to_dict(self) -> dict[str, str | dict[str, str]]:
        return {
            "job_id": self.job_id,
            "created_at": self.created_at,
            "profile_name": self.profile_name,
            "app_version": self.app_version,
            "status": self.status.value,
            "config_snapshot": self.config_snapshot,
        }
