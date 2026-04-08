from __future__ import annotations

from backend.app.models.analysis import AnalysisResult
from backend.app.schemas.response_schema import AnalyzeResponse, DifficultWordSchema
from backend.app.services.level_service import LevelService
from backend.app.services.simplification_service import SimplificationService
from backend.app.services.vocab_service import VocabularyService


class AdaptiveService:
	def __init__(
		self,
		level_service: LevelService | None = None,
		simplification_service: SimplificationService | None = None,
		vocab_service: VocabularyService | None = None,
	) -> None:
		self.level_service = level_service or LevelService()
		self.vocab_service = vocab_service or VocabularyService()
		self.simplification_service = simplification_service or SimplificationService(self.vocab_service)

	def analyze(self, text: str) -> AnalyzeResponse:
		level = self.level_service.predict_level(text)
		simplified_text = self.simplification_service.simplify_text(text)
		difficult_words = self.vocab_service.extract_difficult_words(text)

		result = AnalysisResult(
			level=level,
			simplified_text=simplified_text,
			difficult_words=difficult_words,
		)

		return AnalyzeResponse(
			level=result.level,
			simplified_text=result.simplified_text,
			difficult_words=[
				DifficultWordSchema(word=item.word, meaning=item.meaning, synonyms=item.synonyms)
				for item in result.difficult_words
			],
		)

