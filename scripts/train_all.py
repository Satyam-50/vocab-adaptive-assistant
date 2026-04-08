from __future__ import annotations

import json
import os

from models.training.train_classifier import train_level_classifier
from models.training.train_simplifier import save_dummy_simplifier
from scripts.preprocess_data import preprocess_training_data


def train_all() -> dict:
	processed_path = preprocess_training_data()
	fast_mode = os.getenv("FAST_TRAINING", "0").lower() in {"1", "true", "yes"}
	metrics = train_level_classifier(processed_path, fast_mode=fast_mode)
	save_dummy_simplifier("models/saved_models/simplifier_model.pt")
	return {
		"processed_data": str(processed_path),
		"fast_mode": fast_mode,
		"classifier_metrics": metrics,
		"simplifier": "saved",
	}


if __name__ == "__main__":
	result = train_all()
	print(json.dumps(result, indent=2))

