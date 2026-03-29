# Sceneqora Plan

## Current stage

Stage 3 focuses on assembling the minimal local pipeline and validating its local outputs.

## Completed tickets

1. `etape_1_001_bootstrap_repo_minimal`
2. `etape_1_002_config_contrats_manifest_minimal`
3. `etape_2_001_probe_video_local_minimal`
4. `etape_2_002_extraction_audio_locale_minimale`
5. `etape_2_003_transcription_audio_locale_minimale`
6. `etape_2_004_horodatage_transcription_audio_minimal`
7. `etape_2_005_generation_srt_minimale`
8. `etape_3_001_assemblage_pipeline_local_minimal`
9. `etape_3_002_validation_output_pipeline_minimale` in local implementation/review state

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
- A minimal local audio transcription capability is implemented on the ticket branch for `etape_2_003`.
- The CLI now also exposes `transcribe-audio` for plain UTF-8 transcript output.
- Deterministic tests mock the STT adapter; the live transcription test remains outside `make check`.
- A minimal local timestamped transcription capability is implemented on the ticket branch for `etape_2_004`.
- The CLI now also exposes `transcribe-audio-timestamps` for minimal JSON segment output.
- Deterministic tests mock the timestamp-capable STT adapter; the live timestamp test remains outside `make check`.
- A minimal local SRT generation capability is implemented on the ticket branch for `etape_2_005`.
- The CLI now also exposes `generate-srt` for deterministic SRT output from timestamped JSON.
- Deterministic tests validate JSON structure and SRT rendering without a real STT engine.
- A minimal local pipeline assembly capability is implemented on the ticket branch for `etape_3_001`.
- The CLI now also exposes `run-local-pipeline` to generate four fixed artifacts in one output directory.
- Deterministic tests stub the stage 2 bricks; the live pipeline run remains outside `make check`.
- A minimal local output validation capability is implemented on the ticket branch for `etape_3_002`.
- The CLI now also exposes `validate-local-pipeline-output` for structural validation of one pipeline output directory.
- Deterministic tests validate file presence, JSON structure, SRT counting, and simple output coherence.

## Next logical step

1. Wait for GPT 5.4 review of `etape_3_002` before any Git sequence.
2. Run the live local output validation test on a real pipeline output directory and include the result in the review loop.

## Guardrails

- Keep the scope local and simple.
- Do not introduce video or AI pipeline logic yet.
- Validate each ticket locally before moving forward.
- Update this file at the end of each ticket.
- Add a validation notebook at the end of each ticket.
