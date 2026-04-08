from __future__ import annotations

import re

from models.inference.predict_level import predict_text_level
from models.inference.simplify_text import COMPLEX_TO_SIMPLE, simplify_text


COMMON_WORDS = {
	"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
	"in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will",
	"with", "this", "these", "those", "you", "your", "we", "they", "their", "or", "but",
	"if", "then", "there", "here", "can", "could", "should", "would", "do", "does", "did",
}

DUMMY_VOCAB_INFO: dict[str, dict[str, list[str] | str]] = {
	"analysis": {"meaning": "careful study", "synonyms": ["study", "review"]},
	"complex": {"meaning": "not easy", "synonyms": ["hard", "complicated"]},
	"significant": {"meaning": "important", "synonyms": ["important", "major"]},
	"utilize": {"meaning": "to use something", "synonyms": ["use", "apply"]},
	"commence": {"meaning": "to begin", "synonyms": ["start", "begin"]},
}


def process_text(text: str) -> dict:
	"""Run complete NLP pipeline: level prediction, simplification, and vocab extraction."""
	if not isinstance(text, str):
		raise TypeError("text must be a string")

	cleaned = text.strip()
	level = predict_text_level(cleaned)
	simplified = simplify_text(cleaned)
	difficult_words = extract_difficult_words(cleaned)

	return {
		"level": level,
		"simplified_text": simplified,
		"difficult_words": difficult_words,
	}


def extract_difficult_words(text: str, limit: int = 8) -> list[dict[str, object]]:
	words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]*", text)]
	seen: set[str] = set()
	results: list[dict[str, object]] = []

	for word in words:
		if word in seen or word in COMMON_WORDS:
			continue
		seen.add(word)

		if word in DUMMY_VOCAB_INFO or len(word) >= 8:
			info = DUMMY_VOCAB_INFO.get(word)
			if info:
				meaning = str(info["meaning"])
				synonyms = list(info["synonyms"])
			else:
				simple = COMPLEX_TO_SIMPLE.get(word, f"simple {word}")
				meaning = "A relatively advanced word from the text."
				synonyms = [simple]

			results.append(
				{
					"word": word,
					"meaning": meaning,
					"synonyms": synonyms,
				}
			)

		if len(results) >= limit:
			break

	return results

