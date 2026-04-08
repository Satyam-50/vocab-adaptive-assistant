from __future__ import annotations

import re


def clean_text(text: str) -> str:
	text = text or ""
	text = text.replace("\n", " ").replace("\t", " ")
	text = re.sub(r"\s+", " ", text)
	return text.strip()


def tokenize_words(text: str) -> list[str]:
	return re.findall(r"[A-Za-z][A-Za-z'-]*", clean_text(text).lower())


def split_sentences(text: str) -> list[str]:
	cleaned = clean_text(text)
	if not cleaned:
		return []
	return [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]


def count_syllables(word: str) -> int:
	word = re.sub(r"[^a-z]", "", word.lower())
	if not word:
		return 0
	vowels = "aeiouy"
	count = 0
	prev_vowel = False
	for ch in word:
		is_vowel = ch in vowels
		if is_vowel and not prev_vowel:
			count += 1
		prev_vowel = is_vowel
	if word.endswith("e") and count > 1:
		count -= 1
	return max(count, 1)

