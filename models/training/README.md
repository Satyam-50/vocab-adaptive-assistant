# Model Training Guide

## Overview

This project includes trainable models for:
1. **Level Classifier** - Predicts CEFR reading difficulty (A1-C2)
2. **Text Simplifier** - Generates simplified versions of input text
3. **Vocabulary Analyzer** - Identifies difficult words and synonyms

## Recent Updates

### Large PDF Support (January 2025)

The training pipeline has been updated to support **large PDF files** with the following capacity limits:
- **Maximum file size**: 200 MB
- **Maximum pages**: 400 pages
- **Maximum extracted characters**: 500,000 characters

These limits are configurable via environment variables in `backend/app/core/config.py`.

### Model Retraining

Models have been freshly trained with the following configuration:
- **Classifier Algorithm**: LogisticRegression (multinomial classification)
- **Feature Generation**: TF-IDF vectorization with bigram/trigram support
- **Training Data**: 40 samples across A1, A2, B1, B2 difficulty levels
- **Test Accuracy**: 50% (on small validation set)

*Note: For production use, provide a larger, more balanced training dataset in `data/raw/` with CSV files containing `text` and `level` columns.*

## Training Setup

### 1. Install Backend Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 2. Install Training Dependencies
```powershell
pip install -r models/training/requirements.txt
```

This installs additional packages including:
- **pandas** - Data processing and feature engineering
- **torch** - Deep learning framework (for simplifier model)
- **pillow, pytesseract** - Image processing for future OCR support
- **nltk** - Natural language processing utilities

### 3. Prepare Training Data

Create CSV files in `data/raw/` with the following structure:

```csv
text,level
The cat is sleeping,A1
She speaks English fluently,A2
The implementation of artificial intelligence has revolutionized various industries,B1
The burgeoning complexities inherent in contemporary socioeconomic structures necessitate sophisticated analytical frameworks,B2
```

**Required columns:**
- `text` (string) - The training example sentence/paragraph
- `level` (string) - CEFR level: A1, A2, B1, B2, C1, or C2

### 4. Train All Models
```powershell
python -m scripts.train_all
```

**Output:**
```json
{
  "processed_data": "data/processed/training_data.csv",
  "classifier_metrics": {
    "accuracy": 0.50,
    "weighted_f1": 0.458,
    "training_seconds": 0.041
  },
  "simplifier": "saved"
}
```

## Model Artifacts

### Saved Files
- `models/saved_models/level_classifier.pkl` - Trained LogisticRegression classifier
- `models/saved_models/vectorizer.pkl` - Fitted TF-IDF vectorizer
- `models/saved_models/simplifier_model.pt` - PyTorch text simplification model
- `data/processed/training_data.csv` - Preprocessed training data

### Loading Models in Backend
The FastAPI backend automatically loads these artifacts on startup via `backend/app/services/level_service.py`:
```python
classifier = joblib.load("models/saved_models/level_classifier.pkl")
vectorizer = joblib.load("models/saved_models/vectorizer.pkl")
```

## Improving Model Performance

### For Better Classification Accuracy:
1. **Increase dataset size** - Use 1,000+ examples per difficulty level
2. **Balance classes** - Ensure equal representation of A1-C2 levels
3. **Add diversity** - Include varied text types (articles, blogs, technical docs)
4. **Tune hyperparameters** - Modify `models/training/config.py`:
   ```python
   class TrainingConfig:
       max_tfidf_features: int = 5000
       n_gram_range: tuple = (1, 3)
       random_state: int = 42
   ```

### For Better Simplification:
1. Implement a full seq2seq model instead of dummy simplifier
2. Consider BART fine-tuning or T5 models
3. Add paired (complex, simple) examples to training data

## Configuration

### PDF Processing Limits
Set via environment variables before backend startup:
```powershell
$env:PDF_MAX_SIZE_MB = "200"
$env:PDF_MAX_PAGES = "400"
$env:PDF_MAX_CHARS = "500000"
```

### Fast Training Mode
For quick development iteration:
```powershell
$env:FAST_TRAINING = "1"
python -m scripts.train_all
```

Uses SGDClassifier instead of LogisticRegression for faster training.

## Troubleshooting

### ModuleNotFoundError: No module named 'pandas'
```powershell
pip install pandas
```

### ModuleNotFoundError: No module named 'torch'
```powershell
pip install torch
```

### FileNotFoundError: No CSV files found in data/raw
Create training CSV files in `data/raw/` with `text` and `level` columns.

### sklearn version incompatibility
Update scikit-learn:
```powershell
pip install --upgrade scikit-learn
```

## API Endpoints

After training, models are used by:
- `POST /analyze` - Classify text and identify difficult words
- `POST /analyze/pdf` - Extract and analyze PDF content with large file support (up to 200 MB)

Example:
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The burgeoning complexities..."}'
```

Response:
```json
{
  "level": "C2",
  "simplified_text": "...",
  "difficult_words": [{"word": "burgeoning", "meaning": "...", "synonyms": "..."}]
}
```

## Future Improvements

- [ ] Implement full neural text simplification model with attention mechanism
- [ ] Add OCR support for handwritten PDFs using pytesseract + Tesseract-OCR
- [ ] Support multiple languages (Spanish, French, Chinese)
- [ ] Add confidence scores to level predictions
- [ ] Implement active learning for continuous model improvement
- [ ] Cache vectorizer results for faster re-analysis of duplicate texts
