from __future__ import annotations

from backend.app.core.constants import CEFR_LEVELS
from backend.app.utils.tokenizer import split_sentences, tokenize_words


def count_syllables(word: str) -> int:
	word = word.lower().strip()
	if not word:
		return 0
	vowels = "aeiouy"
	count = 0
	previous_is_vowel = False
	for character in word:
		is_vowel = character in vowels
		if is_vowel and not previous_is_vowel:
			count += 1
		previous_is_vowel = is_vowel
	if word.endswith("e") and count > 1:
		count -= 1
	return max(count, 1)


def is_complex_word(word: str) -> bool:
	return len(word) >= 8 or count_syllables(word) >= 3


def readability_profile(text: str) -> dict[str, float]:
	words = tokenize_words(text)
	sentences = split_sentences(text)
	sentence_count = max(len(sentences), 1)
	word_count = max(len(words), 1)
	average_sentence_length = word_count / sentence_count
	average_word_length = sum(len(word) for word in words) / word_count if words else 0.0
	complex_word_count = sum(1 for word in words if is_complex_word(word))
	complex_ratio = complex_word_count / word_count
	score = (average_sentence_length * 1.5) + (average_word_length * 1.2) + (complex_ratio * 10)
	return {
		"sentence_count": float(sentence_count),
		"word_count": float(word_count),
		"average_sentence_length": average_sentence_length,
		"average_word_length": average_word_length,
		"complex_ratio": complex_ratio,
		"score": score,
	}


def estimate_level_from_readability(text: str) -> str:
	profile = readability_profile(text)
	score = profile["score"]
	if score < 10:
		return "A1"
	if score < 13:
		return "A2"
	if score < 16:
		return "B1"
	if score < 19:
		return "B2"
	if score < 23:
		return "C1"
	return "C2"


def clamp_level(level: str) -> str:
	normalized = (level or "").upper().strip()
	return normalized if normalized in CEFR_LEVELS else "B1"

