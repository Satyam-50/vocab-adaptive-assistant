from __future__ import annotations

from backend.app.core.constants import COMMON_WORDS, MAX_DIFFICULT_WORDS, VOCABULARY_BANK
from backend.app.models.analysis import VocabularyEntry
from backend.app.utils.readability import is_complex_word
from backend.app.utils.tokenizer import tokenize_words, unique_preserve_order


class VocabularyService:
	def extract_difficult_words(self, text: str) -> list[VocabularyEntry]:
		normalized_words = [word.lower() for word in tokenize_words(text)]
		difficult_candidates: list[str] = []
		for word in normalized_words:
			if word in COMMON_WORDS:
				continue
			if word in difficult_candidates:
				continue
			if word in VOCABULARY_BANK or is_complex_word(word):
				difficult_candidates.append(word)

		ordered_candidates = unique_preserve_order(difficult_candidates)[:MAX_DIFFICULT_WORDS]
		return [self._build_entry(word) for word in ordered_candidates]

	def _build_entry(self, word: str) -> VocabularyEntry:
		metadata = VOCABULARY_BANK.get(word)
		if metadata:
			meaning = str(metadata["meaning"])
			synonyms = list(metadata["synonyms"])
		else:
			meaning = "A less common or more advanced word used in the text."
			synonyms = self._fallback_synonyms(word)
		return VocabularyEntry(word=word, meaning=meaning, synonyms=synonyms)

	def _fallback_synonyms(self, word: str) -> list[str]:
		base = word.rstrip("s") or word
		generated = [f"simple {base}", f"basic {base}"]
		return generated

	def replacement_map(self) -> dict[str, str]:
		return {word: str(details["synonyms"][0]) for word, details in VOCABULARY_BANK.items()}

