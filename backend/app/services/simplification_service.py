from __future__ import annotations

import re

from backend.app.core.constants import LONG_SENTENCE_WORD_COUNT, SIMPLIFICATION_MAP
from backend.app.services.vocab_service import VocabularyService
from backend.app.utils.helpers import preserve_case
from backend.app.utils.tokenizer import split_sentences, tokenize_words, normalize_text


class SimplificationService:
	def __init__(self, vocabulary_service: VocabularyService | None = None) -> None:
		self.vocabulary_service = vocabulary_service or VocabularyService()

	def simplify_text(self, text: str) -> str:
		cleaned_text = normalize_text(text)
		if not cleaned_text:
			return ""

		simplified_text = self._replace_complex_words(cleaned_text)
		simplified_text = self._shorten_long_sentences(simplified_text)
		simplified_text = self._normalize_spacing(simplified_text)
		return simplified_text

	def _replace_complex_words(self, text: str) -> str:
		replacement_map = self.vocabulary_service.replacement_map()

		def substitute(match: re.Match[str]) -> str:
			word = match.group(0)
			lowered = word.lower()
			replacement = replacement_map.get(lowered) or SIMPLIFICATION_MAP.get(lowered)
			if not replacement:
				return word
			return preserve_case(word, replacement)

		return re.sub(r"\b[A-Za-z][A-Za-z'-]*\b", substitute, text)

	def _shorten_long_sentences(self, text: str) -> str:
		sentences = split_sentences(text)
		if not sentences:
			return text

		shortened_sentences: list[str] = []
		for sentence in sentences:
			words = tokenize_words(sentence)
			if len(words) <= LONG_SENTENCE_WORD_COUNT:
				shortened_sentences.append(sentence)
				continue

			pieces = [piece.strip() for piece in re.split(r"[,;:]+", sentence) if piece.strip()]
			if len(pieces) == 1:
				pieces = [piece.strip() for piece in re.split(r"\b(?:and|but|because|while|which|that)\b", sentence) if piece.strip()]

			for piece in pieces:
				shortened_sentences.append(piece.rstrip(".?!") + ".")

		return " ".join(shortened_sentences)

	def _normalize_spacing(self, text: str) -> str:
		text = re.sub(r"\s+([,.;:!?])", r"\1", text)
		text = re.sub(r"\s{2,}", " ", text)
		return text.strip()

