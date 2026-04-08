# Architecture

## High-level flow

1. User submits text from frontend.
2. Backend endpoint `/analyze` receives request.
3. Adaptive service runs:
	- CEFR level prediction (local classifier + fallback readability heuristic)
	- Rule-based simplification
	- Difficult word extraction with local vocabulary bank
4. Structured JSON is returned to frontend.

## Layers

- `backend/app/api/routes`: HTTP routes
- `backend/app/schemas`: request/response validation
- `backend/app/services`: business logic
- `backend/app/utils`: tokenization/readability/helpers
- `models/inference`: standalone NLP inference functions
- `models/training`: training workflows and artifact generation
- `frontend/src`: React UI and local progress tracking

## Storage strategy

- Model artifacts in `models/saved_models`
- Processed datasets in `data/processed`
- Training metrics in `data/interim`

