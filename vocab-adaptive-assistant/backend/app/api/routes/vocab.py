from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/vocab", tags=["vocab"])


@router.get("/health")
def vocab_health() -> dict[str, str]:
	return {"status": "ok"}

