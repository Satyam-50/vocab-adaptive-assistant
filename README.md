# Vocabulary Level Adaptive Reading Assistant

An offline-first NLP system that predicts text difficulty, simplifies content, and highlights difficult vocabulary for learners.

## Core features

- CEFR level prediction (`A1` to `C2`) with local model artifacts
- Rule-based text simplification
- Difficult word extraction with local meanings and synonyms
- React frontend with reading lab and progress dashboard

## Backend run

1. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

2. Run API:

```bash
uvicorn backend.app.main:app --reload
```

## Frontend run

1. Install dependencies:

```bash
cd frontend-new
npm install
```

2. Start:

```bash
npm run dev
```

## Training pipeline

Standard training:

```bash
python scripts/train_all.py
```

Faster training for heavy datasets (Windows PowerShell):

```powershell
$env:FAST_TRAINING="1"
python scripts/train_all.py
```

This command preprocesses data, trains the level classifier, and saves model artifacts. In fast mode, the trainer uses a faster SGD-based path and capped train sampling for large corpora.

## Docker

```bash
docker compose up --build
```

## Project structure

- `backend/`: FastAPI app
- `frontend-new/`: React app
- `models/`: training + inference + saved artifacts
- `scripts/`: automation utilities
- `utils/`: shared NLP helpers

# 📘 Vocabulary Level Adaptive Reading Assistant

## 🚀 Overview

The **Vocabulary Level Adaptive Reading Assistant** is an end-to-end NLP-based system that analyzes a user's input text, determines its difficulty level, simplifies it, and helps users learn new vocabulary interactively.

This project is built **without using any external APIs**, ensuring that all models and logic run locally.

---

## 🎯 Objectives

* Detect reading difficulty level (A1–C2)
* Simplify complex text into easier language
* Highlight difficult words with meanings and synonyms
* Track user learning progress
* Provide adaptive learning experience

---

## 🧠 Key Features

### 1. 📊 Text Difficulty Detection

* Classifies input text into CEFR levels (A1–C2)
* Uses ML model (TF-IDF + Logistic Regression)

---

### 2. 🔄 Text Simplification

* Converts complex sentences into simpler versions
* Uses rule-based and NLP techniques

---

### 3. 📚 Vocabulary Assistance

* Identifies difficult words
* Provides:

  * Meaning
  * Synonyms
  * Context usage

---

### 4. 📈 Adaptive Learning System

* Tracks user performance
* Adjusts difficulty level dynamically

---

### 5. 🧪 Quiz & Feedback

* Generates simple quizzes after reading
* Helps reinforce learning

---

## 🏗️ Project Architecture

```
User Input → Backend (FastAPI) → ML Models → Processing → Response → Frontend UI
```

---

## 📁 Folder Structure

```
vocab-adaptive-assistant/
│
├── data/                # Raw and processed datasets
├── notebooks/           # EDA and experiments
├── models/              # ML models (training + inference)
├── backend/             # FastAPI backend
├── frontend-new/        # React frontend
├── utils/               # Shared utilities
├── config/              # Config files
├── scripts/             # Automation scripts
├── docs/                # Documentation
```

---

## ⚙️ Tech Stack

### 🔹 Backend

* FastAPI
* Python

### 🔹 Machine Learning

* Scikit-learn
* NLTK / spaCy

### 🔹 Frontend

* React.js
* HTML, CSS, JavaScript

---

## 🧠 Machine Learning Pipeline

1. Text preprocessing
2. Feature extraction (TF-IDF)
3. Level classification
4. Text simplification
5. Vocabulary extraction

---

## 🔌 API Endpoints

### 🔹 Health Check

```
GET /health
```

### 🔹 Analyze Text

```
POST /analyze
```

#### Request:

```json
{
  "text": "Your input text"
}
```

#### Response:

```json
{
  "level": "B2",
  "simplified_text": "Simplified version",
  "difficult_words": [
    {
      "word": "proliferation",
      "meaning": "rapid increase",
      "synonyms": ["growth", "expansion"]
    }
  ]
}
```

### 🔹 Analyze PDF

```
POST /analyze/pdf
```

`multipart/form-data` body key: `pdf_file`

---

## ▶️ How to Run

### 1. Clone the Repository

```
git clone <repo-url>
cd vocab-adaptive-assistant
```

### 2. Install Dependencies

```
pip install -r backend/requirements.txt
```

### 3. Run Backend Server

```
uvicorn backend.app.main:app --reload
```

### 4. Run Frontend

```
cd frontend-new
npm install
npm run dev
```

---

## 📊 Future Improvements

* Transformer-based text simplification
* Personalized learning paths
* Speech support (Text-to-Speech)
* Advanced analytics dashboard

---

## 💡 Key Highlights

* Fully offline system (no external API)
* End-to-end ML pipeline
* Modular and scalable architecture
* Real-world NLP application

---

## 👨‍💻 Author

**Satyam Vishwakarma**
CSE Student, NIT Jamshedpur

---

## ⭐ Contribution

Feel free to fork and contribute to improve this project!
