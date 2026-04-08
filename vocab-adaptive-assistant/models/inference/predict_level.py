from __future__ import annotations

import pickle
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "saved_models" / "level_classifier.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "saved_models" / "vectorizer.pkl"
LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")

_MODEL: Any | None = None
_VECTORIZER: Any | None = None
_LOAD_ATTEMPTED = False


def predict_text_level(text: str) -> str:
	"""Predict CEFR level using local model artifacts, with a heuristic fallback."""
	cleaned = (text or "").strip()
	if not cleaned:
		return "A1"

	_load_model_once()

	if _MODEL is not None and hasattr(_MODEL, "predict"):
		features = _build_features(cleaned)
		for feature in features:
			try:
				prediction = _MODEL.predict(feature)[0]
				level = _normalize_prediction(prediction)
				if level:
					return level
			except Exception:
				continue

	return _heuristic_level(cleaned)


def _load_model_once() -> None:
	global _LOAD_ATTEMPTED, _MODEL, _VECTORIZER
	if _LOAD_ATTEMPTED:
		return
	_LOAD_ATTEMPTED = True

	try:
		if MODEL_PATH.exists():
			with MODEL_PATH.open("rb") as f:
				_MODEL = pickle.load(f)
	except Exception:
		_MODEL = None

	try:
		if VECTORIZER_PATH.exists():
			with VECTORIZER_PATH.open("rb") as f:
				_VECTORIZER = pickle.load(f)
	except Exception:
		_VECTORIZER = None


def _build_features(text: str) -> list[Any]:
	inputs: list[Any] = []
	if _VECTORIZER is not None and hasattr(_VECTORIZER, "transform"):
		try:
			inputs.append(_VECTORIZER.transform([text]))
		except Exception:
			pass
	inputs.append([text])
	return inputs


def _normalize_prediction(prediction: Any) -> str | None:
	if isinstance(prediction, str):
		candidate = prediction.strip().upper()
		return candidate if candidate in LEVELS else None

	try:
		index = int(prediction)
	except (TypeError, ValueError):
		return None

	if 0 <= index < len(LEVELS):
		return LEVELS[index]
	if 1 <= index <= len(LEVELS):
		return LEVELS[index - 1]
	return None


def _heuristic_level(text: str) -> str:
	words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
	sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
	if not words:
		return "A1"

	avg_word_len = sum(len(w) for w in words) / len(words)
	avg_sentence_len = len(words) / max(len(sentences), 1)
	long_word_ratio = sum(1 for w in words if len(w) >= 8) / len(words)

	score = (avg_word_len * 1.1) + (avg_sentence_len * 0.65) + (long_word_ratio * 12)
    
	if score < 9:
		return "A1"
	if score < 11:
		return "A2"
	if score < 13:
		return "B1"
	if score < 15:
		return "B2"
	if score < 17:
		return "C1"
	return "C2"

