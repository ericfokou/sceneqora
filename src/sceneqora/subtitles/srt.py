"""Minimal SRT generation from timestamped transcript JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sceneqora.domain import GeneratedSrtArtifact


class SrtGenerationError(RuntimeError):
    """Raised when minimal SRT generation fails."""


def generate_srt(source_path: str | Path, output_path: str | Path) -> GeneratedSrtArtifact:
    source = Path(source_path)
    output = Path(output_path)

    payload = _load_timestamped_json(source)
    segments = _validate_segments(source=source, payload=payload)
    srt_content = _render_srt(segments=segments)
    _write_srt(output=output, content=srt_content)

    if not output.exists():
        raise SrtGenerationError(f"expected output was not created at '{output}'")

    return GeneratedSrtArtifact.create(
        source_path=source,
        output_path=output,
        subtitle_count=len(segments),
    )


def _load_timestamped_json(source: Path) -> dict[str, Any]:
    if not source.exists():
        raise SrtGenerationError(f"source transcript JSON was not found at '{source}'")

    if not source.is_file():
        raise SrtGenerationError(f"source transcript JSON is not a file: '{source}'")

    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SrtGenerationError(f"invalid JSON in '{source}'") from exc
    except OSError as exc:
        raise SrtGenerationError(f"could not read transcript JSON from '{source}': {exc}") from exc

    if not isinstance(payload, dict):
        raise SrtGenerationError(f"invalid transcript JSON structure in '{source}'")

    return payload


def _validate_segments(*, source: Path, payload: dict[str, Any]) -> list[dict[str, float | str]]:
    raw_segments = payload.get("segments")
    if not isinstance(raw_segments, list):
        raise SrtGenerationError(f"missing or invalid 'segments' in '{source}'")

    segments: list[dict[str, float | str]] = []
    for raw_segment in raw_segments:
        if not isinstance(raw_segment, dict):
            raise SrtGenerationError(f"invalid segment payload in '{source}'")

        try:
            start = float(raw_segment["start"])
            end = float(raw_segment["end"])
            text = str(raw_segment["text"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SrtGenerationError(f"invalid segment payload in '{source}'") from exc

        if end < start:
            raise SrtGenerationError(f"invalid segment timing in '{source}': end before start")

        segments.append({"start": start, "end": end, "text": text})

    return segments


def _render_srt(*, segments: list[dict[str, float | str]]) -> str:
    blocks: list[str] = []

    for index, segment in enumerate(segments, start=1):
        start = _format_srt_timestamp(float(segment["start"]))
        end = _format_srt_timestamp(float(segment["end"]))
        text = str(segment["text"])
        blocks.append(f"{index}\n{start} --> {end}\n{text}")

    if not blocks:
        return ""

    return "\n\n".join(blocks) + "\n\n"


def _format_srt_timestamp(seconds: float) -> str:
    total_milliseconds = int(round(seconds * 1000))

    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1_000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def _write_srt(*, output: Path, content: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        output.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise SrtGenerationError(f"could not write SRT to '{output}': {exc}") from exc
