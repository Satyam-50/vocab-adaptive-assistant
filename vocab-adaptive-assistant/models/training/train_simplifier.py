from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class DummySimplifierModel:
	replacements: dict[str, str]


def build_rule_based_simplifier() -> DummySimplifierModel:
	# Placeholder artifact for offline deployment checks.
	replacements = {
		"utilize": "use",
		"commence": "start",
		"terminate": "end",
		"demonstrate": "show",
		"subsequent": "next",
	}
	return DummySimplifierModel(replacements=replacements)


def save_dummy_simplifier(path: str) -> None:
	model = build_rule_based_simplifier()
	torch.save({"replacements": model.replacements}, path)


if __name__ == "__main__":
	save_dummy_simplifier("models/saved_models/simplifier_model.pt")
	print("Saved rule-based simplifier artifact")

