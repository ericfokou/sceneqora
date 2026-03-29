"""Minimal CLI entrypoint for the Sceneqora bootstrap stage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sceneqora import __version__
from sceneqora.domain.manifests import JobManifest
from sceneqora.ingestion import extract_audio, inspect_video
from sceneqora.ingestion.audio import AudioExtractionError
from sceneqora.ingestion.probe import ProbeError
from sceneqora.infra.config import load_app_config
from sceneqora.transcription import (
    AudioTranscriptionError,
    transcribe_audio,
    transcribe_audio_timestamps,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sceneqora",
        description="Sceneqora bootstrap CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "inspect",
        help="Load the default config and print a minimal job manifest.",
    )
    inspect_video_parser = subparsers.add_parser(
        "inspect-video",
        help="Probe a local video and print a normalized VideoAsset JSON payload.",
    )
    inspect_video_parser.add_argument("source_path", type=Path, help="Path to the local video file.")
    extract_audio_parser = subparsers.add_parser(
        "extract-audio",
        help="Extract audio from a local video into a WAV PCM mono 16 kHz file.",
    )
    extract_audio_parser.add_argument("source_path", type=Path, help="Path to the local video file.")
    extract_audio_parser.add_argument("output_path", type=Path, help="Path to the output WAV file.")
    transcribe_audio_parser = subparsers.add_parser(
        "transcribe-audio",
        help="Transcribe a local WAV file into a plain UTF-8 text file.",
    )
    transcribe_audio_parser.add_argument("source_path", type=Path, help="Path to the local WAV file.")
    transcribe_audio_parser.add_argument("output_path", type=Path, help="Path to the output TXT file.")
    transcribe_audio_timestamps_parser = subparsers.add_parser(
        "transcribe-audio-timestamps",
        help="Transcribe a local WAV file into a minimal timestamped JSON artifact.",
    )
    transcribe_audio_timestamps_parser.add_argument(
        "source_path",
        type=Path,
        help="Path to the local WAV file.",
    )
    transcribe_audio_timestamps_parser.add_argument(
        "output_path",
        type=Path,
        help="Path to the output JSON file.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the bootstrap version and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"sceneqora {__version__}")
        return 0

    if args.command == "inspect":
        config = load_app_config()
        manifest = JobManifest.bootstrap(config=config, app_version=__version__)
        print(json.dumps(manifest.to_dict(), indent=2))
        return 0

    if args.command == "inspect-video":
        try:
            video_asset = inspect_video(args.source_path)
        except ProbeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(video_asset.to_dict(), indent=2))
        return 0

    if args.command == "extract-audio":
        try:
            extracted_audio = extract_audio(args.source_path, args.output_path)
        except AudioExtractionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(extracted_audio.to_dict(), indent=2))
        return 0

    if args.command == "transcribe-audio":
        try:
            transcript_artifact = transcribe_audio(args.source_path, args.output_path)
        except AudioTranscriptionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(transcript_artifact.to_dict(), indent=2))
        return 0

    if args.command == "transcribe-audio-timestamps":
        try:
            timestamped_artifact = transcribe_audio_timestamps(args.source_path, args.output_path)
        except AudioTranscriptionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(timestamped_artifact.to_cli_dict(), indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
