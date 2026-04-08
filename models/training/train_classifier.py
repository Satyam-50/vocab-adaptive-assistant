from __future__ import annotations

import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from models.training.config import TRAINING_CONFIG
from utils.evaluation_metrics import evaluate_classifier


CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def train_level_classifier(data_path: Path | None = None, fast_mode: bool = False) -> dict:
	config = TRAINING_CONFIG
	data_file = data_path or config.processed_data_path
	if not data_file.exists():
		raise FileNotFoundError(f"Training data not found at {data_file}")
	start_time = time.perf_counter()

	df = pd.read_csv(data_file)
	if "text" not in df or "level" not in df:
		raise ValueError("training_data.csv must include 'text' and 'level' columns")

	df = df[df["level"].isin(CEFR_LEVELS)].dropna(subset=["text", "level"])
	X_train, X_test, y_train, y_test = train_test_split(
		df["text"],
		df["level"],
		test_size=config.test_size,
		random_state=config.random_state,
		stratify=df["level"],
	)

	if fast_mode and len(X_train) > config.fast_mode_max_train_samples:
		X_train, _, y_train, _ = train_test_split(
			X_train,
			y_train,
			train_size=config.fast_mode_max_train_samples,
			random_state=config.random_state,
			stratify=y_train,
		)

	if fast_mode:
		tfidf = TfidfVectorizer(
			max_features=config.fast_mode_max_tfidf_features,
			ngram_range=config.fast_mode_n_gram_range,
			strip_accents="unicode",
			lowercase=True,
			dtype=np.float32,
			sublinear_tf=True,
		)
		classifier = SGDClassifier(
			loss="log_loss",
			alpha=config.sgd_alpha,
			max_iter=config.sgd_max_iter,
			random_state=config.random_state,
			early_stopping=True,
			validation_fraction=0.1,
			n_jobs=-1,
		)
		algorithm = "sgd"
	else:
		tfidf = TfidfVectorizer(
			max_features=config.max_tfidf_features,
			ngram_range=config.n_gram_range,
			strip_accents="unicode",
			lowercase=True,
			dtype=np.float32,
			sublinear_tf=True,
		)
		classifier = LogisticRegression(
			max_iter=2000,
			multi_class="multinomial",
			random_state=config.random_state,
			C=2.0,
			solver="saga",
			n_jobs=-1,
		)
		algorithm = "logreg"

	pipeline = Pipeline(
		steps=[
			("tfidf", tfidf),
			("clf", classifier),
		],
	)

	pipeline.fit(X_train, y_train)
	y_pred = pipeline.predict(X_test)
	metrics = evaluate_classifier(y_test.tolist(), y_pred.tolist())

	config.model_output_dir.mkdir(parents=True, exist_ok=True)
	tfidf = pipeline.named_steps["tfidf"]
	clf = pipeline.named_steps["clf"]

	joblib.dump(clf, config.model_output_dir / "level_classifier.pkl")
	joblib.dump(tfidf, config.model_output_dir / "vectorizer.pkl")

	config.log_path.parent.mkdir(parents=True, exist_ok=True)
	metrics["training_seconds"] = round(time.perf_counter() - start_time, 3)
	metrics["algorithm"] = algorithm
	metrics["train_samples"] = int(len(X_train))
	metrics["test_samples"] = int(len(X_test))
	with config.log_path.open("w", encoding="utf-8") as fp:
		json.dump(metrics, fp, indent=2)

	return metrics


if __name__ == "__main__":
	result = train_level_classifier()
	print(json.dumps(result, indent=2))

