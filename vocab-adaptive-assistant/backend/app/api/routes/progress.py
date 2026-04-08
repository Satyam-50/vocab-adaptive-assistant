from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/health")
def progress_health() -> dict[str, str]:
	return {"status": "ok"}

