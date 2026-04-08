from __future__ import annotations

import re


COMPLEX_TO_SIMPLE: dict[str, str] = {
	"utilize": "use",
	"commence": "start",
	"terminate": "end",
	"demonstrate": "show",
	"approximately": "about",
	"subsequent": "next",
	"assistance": "help",
	"individuals": "people",
	"purchase": "buy",
	"residence": "home",
	"objective": "goal",
	"obtain": "get",
	"require": "need",
	"difficult": "hard",
	"significant": "important",
}

WORD_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
LONG_SENTENCE_LIMIT = 18


def simplify_text(text: str) -> str:
	"""Simplify text by replacing complex words and splitting long sentences."""
	if not text or not text.strip():
		return ""

	cleaned = re.sub(r"\s+", " ", text).strip()
	replaced = _replace_complex_words(cleaned)
	shortened = _split_long_sentences(replaced)
	return re.sub(r"\s+", " ", shortened).strip()


def _replace_complex_words(text: str) -> str:
	def repl(match: re.Match[str]) -> str:
		word = match.group(0)
		replacement = COMPLEX_TO_SIMPLE.get(word.lower())
		if not replacement:
			return word
		if word.isupper():
			return replacement.upper()
		if word[0].isupper():
			return replacement.capitalize()
		return replacement

	return WORD_PATTERN.sub(repl, text)


def _split_long_sentences(text: str) -> str:
	sentences = [s.strip() for s in SENTENCE_SPLIT_PATTERN.split(text) if s.strip()]
	if not sentences:
		return text

	result: list[str] = []
	for sentence in sentences:
		word_count = len(re.findall(r"[A-Za-z][A-Za-z'-]*", sentence))
		if word_count <= LONG_SENTENCE_LIMIT:
			result.append(sentence)
			continue

		parts = [p.strip() for p in re.split(r"[,;:]+", sentence) if p.strip()]
		if len(parts) == 1:
			parts = [
				p.strip()
				for p in re.split(r"\b(?:and|but|because|which|that|while)\b", sentence)
				if p.strip()
			]

		if len(parts) <= 1:
			result.append(sentence)
			continue

		for part in parts:
			result.append(part.rstrip(".?!") + ".")

	return " ".join(result)

