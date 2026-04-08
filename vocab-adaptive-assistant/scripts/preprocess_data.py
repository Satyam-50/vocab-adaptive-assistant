from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.text_processing import clean_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "training_data.csv"


def preprocess_training_data() -> Path:
	PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

	raw_files = list(RAW_DIR.glob("*.csv"))
	if not raw_files:
		raise FileNotFoundError("No CSV files found in data/raw")

	frames: list[pd.DataFrame] = []
	for file_path in raw_files:
		df = pd.read_csv(file_path)
		if "text" in df.columns and "level" in df.columns:
			frames.append(df[["text", "level"]].copy())

	if not frames:
		raise ValueError("No valid CSV with 'text' and 'level' columns found")

	merged = pd.concat(frames, ignore_index=True)
	merged["text"] = merged["text"].astype(str).map(clean_text)
	merged["level"] = merged["level"].astype(str).str.upper().str.strip()
	merged = merged[(merged["text"].str.len() > 0) & (merged["level"].str.len() > 0)]
	merged = merged.drop_duplicates(subset=["text", "level"])

	merged.to_csv(OUTPUT_FILE, index=False)
	return OUTPUT_FILE


if __name__ == "__main__":
	output = preprocess_training_data()
	print(f"Processed dataset saved to: {output}")

