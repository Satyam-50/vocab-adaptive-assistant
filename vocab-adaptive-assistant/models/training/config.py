from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TrainingConfig:
	random_state: int = 42
	test_size: float = 0.2
	max_tfidf_features: int = 15000
	n_gram_range: tuple[int, int] = (1, 2)
	model_output_dir: Path = PROJECT_ROOT / "models" / "saved_models"
	processed_data_path: Path = PROJECT_ROOT / "data" / "processed" / "training_data.csv"
	log_path: Path = PROJECT_ROOT / "data" / "interim" / "training_metrics.json"


TRAINING_CONFIG = TrainingConfig()

