from __future__ import annotations

from functools import lru_cache

from backend.app.services.adaptive_service import AdaptiveService
from backend.app.services.level_service import LevelService
from backend.app.services.simplification_service import SimplificationService
from backend.app.services.vocab_service import VocabularyService


@lru_cache(maxsize=1)
def get_level_service() -> LevelService:
	return LevelService()


@lru_cache(maxsize=1)
def get_vocab_service() -> VocabularyService:
	return VocabularyService()


@lru_cache(maxsize=1)
def get_simplification_service() -> SimplificationService:
	return SimplificationService(get_vocab_service())


@lru_cache(maxsize=1)
def get_adaptive_service() -> AdaptiveService:
	return AdaptiveService(
		level_service=get_level_service(),
		simplification_service=get_simplification_service(),
		vocab_service=get_vocab_service(),
	)

