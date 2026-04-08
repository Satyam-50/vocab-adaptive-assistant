from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.app.core.constants import CEFR_LEVELS, DEFAULT_LEVEL
from backend.app.core.config import settings
from backend.app.utils.helpers import load_pickle_artifact
from backend.app.utils.readability import estimate_level_from_readability, clamp_level


class LevelService:
	def __init__(self) -> None:
		self.model = self._load_artifact(settings.level_classifier_path)
		self.vectorizer = self._load_artifact(settings.vectorizer_path)

	def _load_artifact(self, path: Path) -> Any:
		if not path.exists():
			return None
		try:
			return load_pickle_artifact(path)
		except Exception:
			return None

	def predict_level(self, text: str) -> str:
		cleaned_text = (text or "").strip()
		if not cleaned_text:
			return DEFAULT_LEVEL

		model_prediction = self._predict_with_model(cleaned_text)
		if model_prediction:
			return model_prediction

		return estimate_level_from_readability(cleaned_text)

	def _predict_with_model(self, text: str) -> str | None:
		if self.model is None or not hasattr(self.model, "predict"):
			return None

		feature_inputs: list[Any] = []
		if self.vectorizer is not None and hasattr(self.vectorizer, "transform"):
			try:
				feature_inputs.append(self.vectorizer.transform([text]))
			except Exception:
				pass
		feature_inputs.append([text])

		for features in feature_inputs:
			try:
				raw_prediction = self.model.predict(features)[0]
				normalized_prediction = self._normalize_prediction(raw_prediction)
				if normalized_prediction:
					return normalized_prediction
			except Exception:
				continue

		return None

	def _normalize_prediction(self, prediction: Any) -> str | None:
		if isinstance(prediction, str):
			candidate = clamp_level(prediction)
			return candidate if candidate in CEFR_LEVELS else None

		try:
			index = int(prediction)
		except (TypeError, ValueError):
			return None

		if 0 <= index < len(CEFR_LEVELS):
			return CEFR_LEVELS[index]
		if 1 <= index <= len(CEFR_LEVELS):
			return CEFR_LEVELS[index - 1]
		return None

