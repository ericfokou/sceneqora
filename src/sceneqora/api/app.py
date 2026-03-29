"""Minimal local FastAPI app for Sceneqora."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sceneqora.app import LocalPipelineRunError, run_local_pipeline


class RunRequest(BaseModel):
    """Minimal request payload for a synchronous local pipeline run."""

    source_path: str
    output_dir: str


def create_app() -> FastAPI:
    """Create the minimal local HTTP API app."""

    api = FastAPI(title="Sceneqora Local API", version="0.1.0")

    @api.exception_handler(RequestValidationError)
    async def handle_request_validation(
        _request: object,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": "invalid request payload", "errors": exc.errors()},
        )

    @api.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.post("/runs")
    async def create_run(payload: RunRequest) -> dict[str, str]:
        source_path = Path(payload.source_path)
        if not source_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"source_path was not found at '{source_path}'",
            )

        try:
            run_result = run_local_pipeline(payload.source_path, payload.output_dir)
        except LocalPipelineRunError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        return run_result.to_dict()

    return api


app = create_app()
