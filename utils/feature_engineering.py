from __future__ import annotations

from utils.text_processing import count_syllables, split_sentences, tokenize_words


def readability_features(text: str) -> dict[str, float]:
	words = tokenize_words(text)
	sentences = split_sentences(text)
	if not words:
		return {
			"word_count": 0.0,
			"sentence_count": 0.0,
			"avg_word_length": 0.0,
			"avg_sentence_length": 0.0,
			"complex_word_ratio": 0.0,
			"avg_syllables": 0.0,
		}

	word_count = len(words)
	sentence_count = max(len(sentences), 1)
	complex_word_count = sum(1 for w in words if len(w) >= 8 or count_syllables(w) >= 3)
	sy_count = sum(count_syllables(w) for w in words)

	return {
		"word_count": float(word_count),
		"sentence_count": float(sentence_count),
		"avg_word_length": sum(len(w) for w in words) / word_count,
		"avg_sentence_length": word_count / sentence_count,
		"complex_word_ratio": complex_word_count / word_count,
		"avg_syllables": sy_count / word_count,
	}

