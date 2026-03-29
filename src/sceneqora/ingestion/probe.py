"""Minimal ffprobe-based video inspection for Sceneqora."""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

from sceneqora.domain import VideoAsset


class ProbeError(RuntimeError):
    """Raised when video probing fails or returns unusable metadata."""


def inspect_video(source_path: str | Path) -> VideoAsset:
    path = Path(source_path)
    payload = _run_ffprobe(path)
    return _parse_video_asset(path=path, payload=payload)


def _run_ffprobe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ProbeError("ffprobe is not available on this machine") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip() or "ffprobe failed"
        raise ProbeError(f"ffprobe error for '{path}': {stderr}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ProbeError(f"invalid ffprobe JSON for '{path}'") from exc

    if not isinstance(payload, dict):
        raise ProbeError(f"unexpected ffprobe payload for '{path}'")

    return payload


def _parse_video_asset(path: Path, payload: dict[str, Any]) -> VideoAsset:
    streams = payload.get("streams")
    if not isinstance(streams, list):
        raise ProbeError(f"missing streams in ffprobe payload for '{path}'")

    format_data = payload.get("format")
    if not isinstance(format_data, dict):
        format_data = {}

    video_stream = next(
        (stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "video"),
        None,
    )
    if video_stream is None:
        raise ProbeError(f"no video stream found for '{path}'")

    audio_stream = next(
        (stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "audio"),
        None,
    )

    duration_sec = _parse_float(video_stream.get("duration"))
    if duration_sec is None:
        duration_sec = _parse_float(format_data.get("duration"))
    if duration_sec is None:
        raise ProbeError(f"missing duration for '{path}'")

    width = _require_int(video_stream.get("width"), field_name="width", path=path)
    height = _require_int(video_stream.get("height"), field_name="height", path=path)
    fps = _parse_fps(video_stream.get("avg_frame_rate"))
    has_audio = True if audio_stream is not None else None
    if any(
        isinstance(stream, dict) and stream.get("codec_type") == "audio"
        for stream in streams
    ):
        has_audio = True
    elif any(
        isinstance(stream, dict) and stream.get("codec_type") == "video"
        for stream in streams
    ):
        has_audio = False
    container = _parse_container(format_data.get("format_name"))

    return VideoAsset.create(
        source_path=path,
        duration_sec=duration_sec,
        width=width,
        height=height,
        fps=fps,
        has_audio=has_audio,
        container=container,
    )


def _require_int(value: Any, *, field_name: str, path: Path) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ProbeError(f"missing {field_name} for '{path}'") from exc


def _parse_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_fps(value: Any) -> float | None:
    if not isinstance(value, str) or value in {"", "0/0"}:
        return None

    try:
        fps = float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None

    return round(fps, 3)


def _parse_container(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None

    return value.split(",")[0].strip()
