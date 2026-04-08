from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
	text: str = Field(..., min_length=1, description="Input text to analyze")

