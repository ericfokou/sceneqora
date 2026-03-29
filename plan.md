# Sceneqora Plan

## Current stage

Stage 1 focuses on a minimal executable repository plus the first configuration and domain contracts.

## Completed tickets

1. `etape_1_001_bootstrap_repo_minimal`
2. `etape_1_002_config_contrats_manifest_minimal`

## Current repo state

- The repo has a minimal Python package under `src/sceneqora`.
- `configs/default.yaml` is the only configuration source.
- The current CLI exposes one inspection mode: `inspect`.
- The current domain nucleus is limited to `AppConfig`, `JobManifest`, and `JobStatus`.
- A validation notebook exists for ticket `etape_1_002`.

## Next logical step

1. Open the next bounded ticket only after GPT 5.4 review of `etape_1_002`.
2. Keep the next ticket outside ingestion, FFmpeg, transcription, scoring, and rendering unless explicitly validated.

## Guardrails

- Keep the scope local and simple.
- Do not introduce video or AI pipeline logic yet.
- Validate each ticket locally before moving forward.
- Update this file at the end of each ticket.
- Add a validation notebook at the end of each ticket.
