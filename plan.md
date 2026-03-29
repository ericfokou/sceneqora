# Sceneqora Plan

## Current stage

Stage 2 focuses on minimal video ingestion, now covering local probe and minimal local audio extraction.

## Completed tickets

1. `etape_1_001_bootstrap_repo_minimal`
2. `etape_1_002_config_contrats_manifest_minimal`
3. `etape_2_001_probe_video_local_minimal`
4. `etape_2_002_extraction_audio_locale_minimale` in local implementation/review state

## Current repo state

- The repo has a minimal Python package under `src/sceneqora`.
- `configs/default.yaml` is the only configuration source.
- The current CLI exposes one inspection mode: `inspect`.
- The current domain nucleus is limited to `AppConfig`, `JobManifest`, and `JobStatus`.
- A validation notebook exists for ticket `etape_1_002`.
- A local `VideoAsset` probe capability is implemented on the ticket branch for `etape_2_001`.
- The CLI now also exposes `inspect-video` for normalized probe output.
- Deterministic tests use mocked or replayed `ffprobe` output; the live probe remains outside `make check`.
- A minimal local audio extraction capability is implemented on the ticket branch for `etape_2_002`.
- The CLI now also exposes `extract-audio` for WAV PCM mono 16 kHz output.
- Deterministic tests mock `ffmpeg`; the real audio extraction remains outside `make check`.

## Next logical step

1. Wait for GPT 5.4 review of `etape_2_002` before any further implementation.
2. Run the live extraction test with real `ffmpeg` and include the result in the review loop.

## Guardrails

- Keep the scope local and simple.
- Do not introduce video or AI pipeline logic yet.
- Validate each ticket locally before moving forward.
- Update this file at the end of each ticket.
- Add a validation notebook at the end of each ticket.
