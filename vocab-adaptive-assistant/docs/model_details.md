# Model Details

## Level detection model

- Primary: TF-IDF + Logistic Regression
- Artifacts:
	- `models/saved_models/level_classifier.pkl`
	- `models/saved_models/vectorizer.pkl`
- Fallback: readability-based heuristic if artifacts are missing/unusable

## Simplification model

- Current production simplifier is rule-based for deterministic offline output.
- Optional artifact `simplifier_model.pt` stores rule map payload.

## Vocabulary extraction

- Uses local curated vocabulary bank and complexity heuristics.
- No external API calls.

