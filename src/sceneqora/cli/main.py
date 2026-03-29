"""Minimal CLI entrypoint for the Sceneqora bootstrap stage."""

from __future__ import annotations

import argparse
import json

from sceneqora import __version__
from sceneqora.domain.manifests import JobManifest
from sceneqora.infra.config import load_app_config


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

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the bootstrap version and exit.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"sceneqora {__version__}")
        return 0

    if args.command == "inspect":
        config = load_app_config()
        manifest = JobManifest.bootstrap(config=config, app_version=__version__)
        print(json.dumps(manifest.to_dict(), indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
