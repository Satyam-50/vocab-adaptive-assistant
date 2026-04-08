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
	pdf_max_size_mb: int = int(os.getenv("PDF_MAX_SIZE_MB", "200"))
	pdf_max_pages: int = int(os.getenv("PDF_MAX_PAGES", "400"))
	pdf_max_chars: int = int(os.getenv("PDF_MAX_CHARS", "500000"))
	cors_allow_origins: tuple[str, ...] = ("*",)
	debug: bool = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes", "on"}


settings = Settings()

