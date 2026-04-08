from __future__ import annotations

from pydantic import BaseModel, Field


class DifficultWordSchema(BaseModel):
	word: str = Field(..., description="The difficult word detected in the text")
	meaning: str = Field(..., description="A short dummy meaning for the word")
	synonyms: list[str] = Field(default_factory=list, description="Simple alternative words")


class AnalyzeResponse(BaseModel):
	level: str = Field(..., description="Predicted CEFR level")
	simplified_text: str = Field(..., description="Simplified version of the input text")
	difficult_words: list[DifficultWordSchema] = Field(default_factory=list)


class HealthResponse(BaseModel):
	status: str = Field(default="ok")

