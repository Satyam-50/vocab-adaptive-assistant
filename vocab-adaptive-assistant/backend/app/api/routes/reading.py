from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.dependencies import get_adaptive_service
from backend.app.schemas.response_schema import AnalyzeResponse
from backend.app.schemas.text_schema import AnalyzeRequest
from backend.app.services.adaptive_service import AdaptiveService


router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest, adaptive_service: AdaptiveService = Depends(get_adaptive_service)) -> AnalyzeResponse:
	if not payload.text.strip():
		raise HTTPException(status_code=400, detail="text must not be empty")
	return adaptive_service.analyze(payload.text)

