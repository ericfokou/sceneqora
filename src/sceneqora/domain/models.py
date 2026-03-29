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


@dataclass(frozen=True, slots=True)
class ExtractedAudio:
    """Minimal contract for a locally extracted WAV audio artifact."""

    source_path: str
    output_path: str
    sample_rate: int
    channels: int
    format: str

    @classmethod
    def create(
        cls,
        source_path: Path,
        output_path: Path,
        *,
        sample_rate: int = 16000,
        channels: int = 1,
        format: str = "wav",
    ) -> "ExtractedAudio":
        return cls(
            source_path=str(source_path),
            output_path=str(output_path),
            sample_rate=sample_rate,
            channels=channels,
            format=format,
        )

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TranscriptionArtifact:
    """Minimal contract for a locally generated transcript text artifact."""

    source_path: str
    output_path: str
    format: str
    engine: str
    status: str

    @classmethod
    def create(
        cls,
        source_path: Path,
        output_path: Path,
        *,
        format: str = "txt",
        engine: str,
        status: str = "completed",
    ) -> "TranscriptionArtifact":
        return cls(
            source_path=str(source_path),
            output_path=str(output_path),
            format=format,
            engine=engine,
            status=status,
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TimestampedTranscriptSegment:
    """Minimal timestamped transcript segment."""

    start: float
    end: float
    text: str

    def to_dict(self) -> dict[str, float | str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TimestampedTranscriptionArtifact:
    """Minimal contract for a locally generated timestamped transcript artifact."""

    source_path: str
    output_path: str
    format: str
    engine: str
    status: str
    segments: list[TimestampedTranscriptSegment]

    @classmethod
    def create(
        cls,
        source_path: Path,
        output_path: Path,
        *,
        engine: str,
        segments: list[TimestampedTranscriptSegment],
        format: str = "json",
    ) -> "TimestampedTranscriptionArtifact":
        status = "completed" if segments else "no_segments"
        return cls(
            source_path=str(source_path),
            output_path=str(output_path),
            format=format,
            engine=engine,
            status=status,
            segments=segments,
        )

    def to_dict(self) -> dict[str, str | list[dict[str, float | str]]]:
        return {
            "source_path": self.source_path,
            "output_path": self.output_path,
            "format": self.format,
            "engine": self.engine,
            "status": self.status,
            "segments": [segment.to_dict() for segment in self.segments],
        }

    def to_cli_dict(self) -> dict[str, str | int]:
        return {
            "source_path": self.source_path,
            "output_path": self.output_path,
            "format": self.format,
            "engine": self.engine,
            "status": self.status,
            "segment_count": len(self.segments),
        }


@dataclass(frozen=True, slots=True)
class GeneratedSrtArtifact:
    """Minimal contract for a locally generated SRT artifact."""

    source_path: str
    output_path: str
    format: str
    status: str
    subtitle_count: int

    @classmethod
    def create(
        cls,
        source_path: Path,
        output_path: Path,
        *,
        subtitle_count: int,
        format: str = "srt",
    ) -> "GeneratedSrtArtifact":
        status = "completed" if subtitle_count > 0 else "no_subtitles"
        return cls(
            source_path=str(source_path),
            output_path=str(output_path),
            format=format,
            status=status,
            subtitle_count=subtitle_count,
        )

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LocalPipelineRunArtifact:
    """Minimal contract for a locally assembled pipeline run."""

    source_path: str
    output_dir: str
    audio_path: str
    transcript_path: str
    segments_path: str
    srt_path: str
    status: str

    @classmethod
    def create(
        cls,
        *,
        source_path: Path,
        output_dir: Path,
        audio_path: Path,
        transcript_path: Path,
        segments_path: Path,
        srt_path: Path,
        status: str = "completed",
    ) -> "LocalPipelineRunArtifact":
        return cls(
            source_path=str(source_path),
            output_dir=str(output_dir),
            audio_path=str(audio_path),
            transcript_path=str(transcript_path),
            segments_path=str(segments_path),
            srt_path=str(srt_path),
            status=status,
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LocalPipelineOutputValidationArtifact:
    """Minimal validation summary for a local pipeline output directory."""

    output_dir: str
    audio_exists: bool
    transcript_exists: bool
    segments_exists: bool
    srt_exists: bool
    segment_count: int
    subtitle_count: int
    status: str

    @classmethod
    def create(
        cls,
        *,
        output_dir: Path,
        audio_exists: bool,
        transcript_exists: bool,
        segments_exists: bool,
        srt_exists: bool,
        segment_count: int,
        subtitle_count: int,
        status: str,
    ) -> "LocalPipelineOutputValidationArtifact":
        return cls(
            output_dir=str(output_dir),
            audio_exists=audio_exists,
            transcript_exists=transcript_exists,
            segments_exists=segments_exists,
            srt_exists=srt_exists,
            segment_count=segment_count,
            subtitle_count=subtitle_count,
            status=status,
        )

    def to_dict(self) -> dict[str, str | bool | int]:
        return asdict(self)
