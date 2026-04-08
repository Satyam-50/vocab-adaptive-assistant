from __future__ import annotations

import re


WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z'-]*")
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def normalize_text(text: str) -> str:
	return re.sub(r"\s+", " ", text or "").strip()


def tokenize_words(text: str) -> list[str]:
	return WORD_PATTERN.findall(text or "")


def split_sentences(text: str) -> list[str]:
	cleaned = normalize_text(text)
	if not cleaned:
		return []
	sentences = SENTENCE_PATTERN.split(cleaned)
	return [sentence.strip() for sentence in sentences if sentence.strip()]


def unique_preserve_order(items: list[str]) -> list[str]:
	seen: set[str] = set()
	ordered: list[str] = []
	for item in items:
		if item in seen:
			continue
		seen.add(item)
		ordered.append(item)
	return ordered

