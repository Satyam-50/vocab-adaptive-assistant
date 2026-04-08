from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
	app_name: str = "Vocabulary Level Adaptive Reading Assistant"
	api_title: str = "Vocabulary Level Adaptive Reading Assistant API"
	api_version: str = "1.0.0"
	project_root: Path = PROJECT_ROOT
	level_classifier_path: Path = PROJECT_ROOT / "models" / "saved_models" / "level_classifier.pkl"
	vectorizer_path: Path = PROJECT_ROOT / "models" / "saved_models" / "vectorizer.pkl"
	simplifier_model_path: Path = PROJECT_ROOT / "models" / "saved_models" / "simplifier_model.pt"
	cors_allow_origins: tuple[str, ...] = ("*",)
	debug: bool = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}


settings = Settings()

