from __future__ import annotations

from typing import Any

from sklearn.metrics import accuracy_score, classification_report, f1_score


def evaluate_classifier(y_true: list[Any], y_pred: list[Any]) -> dict[str, Any]:
	return {
		"accuracy": float(accuracy_score(y_true, y_pred)),
		"weighted_f1": float(f1_score(y_true, y_pred, average="weighted")),
		"report": classification_report(y_true, y_pred, output_dict=True),
	}

