"""Minimal local packaging for one pipeline run output."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from sceneqora.domain import PackagedRunArtifact


EXPECTED_RUN_FILES = [
    "audio.wav",
    "transcript.txt",
    "transcript_segments.json",
    "subtitles.srt",
]


class RunOutputPackagingError(RuntimeError):
    """Raised when a run output cannot be packaged into a minimal zip archive."""


def package_run_output(output_dir: Path, archive_path: Path) -> PackagedRunArtifact:
    """Package one local pipeline output directory into a minimal zip archive."""

    if not output_dir.exists() or not output_dir.is_dir():
        raise RunOutputPackagingError("source output dir was not found")

    if archive_path.suffix.lower() != ".zip":
        raise RunOutputPackagingError("archive path must use the .zip format")

    missing_files = [name for name in EXPECTED_RUN_FILES if not (output_dir / name).is_file()]
    if missing_files:
        raise RunOutputPackagingError(
            "source output dir is missing expected artifacts: " + ", ".join(missing_files)
        )

    try:
        with ZipFile(archive_path, mode="w", compression=ZIP_DEFLATED) as archive:
            for filename in EXPECTED_RUN_FILES:
                archive.write(output_dir / filename, arcname=filename)
    except OSError as exc:
        raise RunOutputPackagingError(f"archive could not be created: {exc}") from exc

    try:
        with ZipFile(archive_path, mode="r") as archive:
            included_files = archive.namelist()
    except OSError as exc:
        raise RunOutputPackagingError(f"archive could not be validated: {exc}") from exc

    if included_files != EXPECTED_RUN_FILES:
        raise RunOutputPackagingError("archive did not contain the expected files")

    return PackagedRunArtifact.create(
        output_dir=output_dir,
        archive_path=archive_path,
        included_files=included_files,
        status="completed",
    )
