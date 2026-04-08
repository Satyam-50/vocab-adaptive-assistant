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
from sklearn.metrics import classification_report, confusion_matrix

from models.training.config import TRAINING_CONFIG
from utils.evaluation_metrics import evaluate_classifier


CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


# ============================================================================
# SYNTHETIC DATA GENERATION
# ============================================================================

def generate_synthetic_training_data() -> pd.DataFrame:
	"""
	Generate synthetic CEFR-labeled training data.
	Creates realistic examples for each difficulty level.
	
	Returns:
		DataFrame with 'text' and 'level' columns
	"""
	synthetic_data = {
		"A1": [
			"I am happy.",
			"She likes cats.",
			"They play football.",
			"The cat is sleeping.",
			"I have a red car.",
			"Do you like coffee?",
			"Where is the bathroom?",
			"I want to learn English.",
			"My name is John.",
			"Hello world.",
			"The weather is nice.",
			"I like to eat pizza.",
			"This is a book.",
			"He goes to school.",
			"We are friends.",
		],
		"A2": [
			"The weather is nice today and I want to go to the park.",
			"She has been studying for three hours.",
			"I prefer tea to coffee.",
			"He is a teacher at the university.",
			"They are discussing the project.",
			"The book is on the shelf.",
			"I haven't seen her since last week.",
			"Could you help me with this problem?",
			"The market is crowded on Sundays.",
			"I can speak English very well.",
			"She used to work in a bank.",
			"The children are playing in the garden.",
			"I would like to learn about history.",
			"Do you have any experience with computers?",
			"The restaurant serves excellent food.",
		],
		"B1": [
			"The implementation of artificial intelligence has revolutionized various industries.",
			"She demonstrated an exceptional comprehension of complex mathematical concepts.",
			"The government implemented comprehensive policies to address environmental concerns.",
			"His dissertation elucidated the intricate mechanisms of neural networks.",
			"The phenomenon exhibits characteristics that warrant further investigation.",
			"Notwithstanding the adverse conditions they persevered determinedly.",
			"The committee deliberated extensively regarding budgetary allocations.",
			"She articulated her position with considerable eloquence.",
			"The economic ramifications of globalization are multifaceted.",
			"The researcher's methodology demonstrated rigorous scientific principles.",
			"These findings corroborate the previous hypothesis about market trends.",
			"The institution has prioritized professional development initiatives.",
			"Despite obstacles, the team accomplished several significant milestones.",
			"The proposal merits careful consideration from stakeholders.",
			"Infrastructure improvements will facilitate smoother operations.",
		],
		"B2": [
			"The burgeoning complexities inherent in contemporary socioeconomic structures necessitate sophisticated analytical frameworks.",
			"His perspicacious observations regarding epistemological paradigms evinced profound scholarly acumen.",
			"The inexorable march of technological advancement precipitates unprecedented paradigmatic transformations.",
			"Notwithstanding the myriad exigencies confronting contemporary societies the resilience demonstrated by communities remains noteworthy.",
			"The obfuscation of empirical data through methodological inconsistencies undermines the veracity of scientific conclusions.",
			"Her circumlocutory discourse obfuscated rather than elucidated the fundamental implications of the proposal.",
			"The proliferation of misinformation necessitates implementation of more sophisticated epistemic safeguards.",
			"The seminal contributions of pioneering researchers fundamentally reconceptualized theoretical frameworks.",
			"The propitious convergence of technological and methodological innovations engendered unprecedented opportunities.",
			"The hegemonic dominance of particular ideological constructs perpetuates systemic inequities.",
			"The juxtaposition of substantive evidence and theoretical speculation illuminates methodological tensions.",
			"Substantive discourse regarding ontological assumptions undergirds contemporary philosophical inquiry.",
			"The amelioration of systemic deficiencies necessitates multidisciplinary collaboration.",
			"Epistemological considerations pervade contemporary scientific methodology.",
			"The dichotomy between empirical observation and theoretical postulation remains unresolved.",
		],
		"C1": [
			"The quintessential manifestation of postmodern epistemology precipitates an inexorable deconstruction of hegemonic paradigmatic assumptions.",
			"The insurmountable antitheses between phenomenological and metaphysical hermeneutics engender profound ontological quandaries.",
			"The obfuscation of metanarrative constructs through polysemantic linguistic instantiation exemplifies contemporary deconstructionist methodology.",
			"The concatenation of socioeconomic variables precipitates multiplicative exacerbation of extant systemic pathologies.",
			"The apotheosis of technological determinism engenders profound existential apprehension regarding anthropogenic modification.",
			"The palliation of persistent epistemic lacunae demands rigorous reconceptualization of foundational theoretical presuppositions.",
			"The amelioration of systemic dysfunctionality necessitates comprehensive reconstitution of institutional frameworks.",
			"The propitious juxtaposition of disparate disciplinary perspectives facilitates unprecedented intellectual convergence.",
			"The exegetical analysis of canonical texts illuminates fundamental tensions within interpretive methodologies.",
			"The pervasive instantiation of algorithmic governance epitomizes the apotheosis of instrumental rationality.",
		],
		"C2": [
			"The quintessential apotheosis of deconstructionist phenomenology instantiates an insurmountable hermeneutical problematic that precipitates irresolvable aporias within the very foundations of epistemological inquiry.",
			"The inexorable concatenation of ontological presuppositions and metaphysical postulations engenders a fundamental aporia that transfigures the categorical architecture of post-structuralist philosophical discourse.",
			"The obfuscation of metanarrative teleology through the polysemantic instantiation of pseudo-linguistic signification epitomizes the apotheosis of postmodern deconstruction.",
			"The apotheosis of biopolitical governmentality precipitates an unprecedented sublation of anthropogenic agency within the architectonic framework of contemporary neoliberal hegemony.",
			"The propitious concatenation of phenomenological hermeneutics and metaphysical exegesis engenders a paradoxical instantiation of epistemological transcendence.",
			"The insurmountable antinomies engendered by the juxtaposition of essentialist ontologies and relativistic epistemologies epitomize the fundamental aporia.",
			"The inexorable march toward totalizing systematicity precipitates the depletion of alterity through the apotheosis of instrumental rationalization.",
		],
	}
	
	# Flatten into DataFrame
	data = []
	for level, texts in synthetic_data.items():
		for text in texts:
			data.append({"text": text, "level": level})
	
	df = pd.DataFrame(data)
	print(f"✓ Generated {len(df)} synthetic training examples")
	print(f"  Samples per level: {df['level'].value_counts().to_dict()}")
	return df


# ============================================================================
# TRAINING FUNCTION
# ============================================================================

def train_level_classifier(data_path: Path | None = None, fast_mode: bool = False, use_synthetic: bool = True) -> dict:
	"""
	Train CEFR level classifier using TF-IDF + Logistic Regression.
	
	Args:
		data_path: Path to CSV with 'text' and 'level' columns
		fast_mode: Use SGD classifier for speed instead of LogisticRegression
		use_synthetic: Generate synthetic data if training data doesn't exist
	
	Returns:
		dict with training metrics, accuracy, and detailed classification report
	"""
	config = TRAINING_CONFIG
	start_time = time.perf_counter()
	
	# Load training data
	data_file = data_path or config.processed_data_path
	
	if data_file.exists():
		print(f"📂 Loading training data from {data_file}")
		df = pd.read_csv(data_file)
	elif use_synthetic:
		print("🤖 Training data not found. Generating synthetic data...")
		df = generate_synthetic_training_data()
	else:
		raise FileNotFoundError(f"Training data not found at {data_file}")
	
	# Validate data
	if "text" not in df.columns or "level" not in df.columns:
		raise ValueError("CSV must include 'text' and 'level' columns")
	
	df = df[df["level"].isin(CEFR_LEVELS)].dropna(subset=["text", "level"])
	print(f"✓ Loaded {len(df)} training examples")
	
	# Split data
	X_train, X_test, y_train, y_test = train_test_split(
		df["text"],
		df["level"],
		test_size=config.test_size,
		random_state=config.random_state,
		stratify=df["level"],
	)
	
	print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
	
	# Apply fast mode sampling if needed
	if fast_mode and len(X_train) > config.fast_mode_max_train_samples:
		X_train, _, y_train, _ = train_test_split(
			X_train,
			y_train,
			train_size=config.fast_mode_max_train_samples,
			random_state=config.random_state,
			stratify=y_train,
		)
		print(f"⚡ Fast mode: sampled to {len(X_train)} training examples")
	
	# Configure vectorizer and classifier
	print("\n🔧 Training model...")
	
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
			random_state=config.random_state,
			C=2.0,
			solver="lbfgs",
		)
		algorithm = "logreg"
	
	# Create pipeline and train
	pipeline = Pipeline(
		steps=[
			("tfidf", tfidf),
			("clf", classifier),
		],
	)
	
	pipeline.fit(X_train, y_train)
	
	# Evaluate
	y_pred = pipeline.predict(X_test)
	metrics = evaluate_classifier(y_test.tolist(), y_pred.tolist())
	
	# Generate detailed classification report
	detailed_report = classification_report(y_test, y_pred, output_dict=True)
	
	# Confusion matrix
	confusion = confusion_matrix(y_test, y_pred, labels=CEFR_LEVELS)
	
	# Save models
	config.model_output_dir.mkdir(parents=True, exist_ok=True)
	tfidf_fitted = pipeline.named_steps["tfidf"]
	clf_fitted = pipeline.named_steps["clf"]
	
	joblib.dump(clf_fitted, config.model_output_dir / "level_classifier.pkl")
	joblib.dump(tfidf_fitted, config.model_output_dir / "vectorizer.pkl")
	
	print(f"\n✅ Model saved to {config.model_output_dir}")
	
	# Prepare final metrics
	training_seconds = round(time.perf_counter() - start_time, 3)
	
	result = {
		**metrics,
		"training_seconds": training_seconds,
		"algorithm": algorithm,
		"train_samples": int(len(X_train)),
		"test_samples": int(len(X_test)),
		"detailed_report": detailed_report,
		"confusion_matrix": confusion.tolist(),
	}
	
	# Save metrics to log file
	config.log_path.parent.mkdir(parents=True, exist_ok=True)
	with config.log_path.open("w", encoding="utf-8") as fp:
		json.dump(result, fp, indent=2)
	
	# Print summary
	print("\n" + "="*60)
	print("TRAINING REPORT")
	print("="*60)
	print(f"Algorithm: {algorithm}")
	print(f"Accuracy: {metrics['accuracy']:.4f}")
	print(f"Weighted F1: {metrics['weighted_f1']:.4f}")
	print(f"Training time: {training_seconds}s")
	print(f"Samples: {len(X_train)} train, {len(X_test)} test")
	print("\nPer-Class Performance:")
	for level in CEFR_LEVELS:
		if level in detailed_report:
			rep = detailed_report[level]
			print(f"  {level}: precision={rep['precision']:.3f}, recall={rep['recall']:.3f}, f1={rep['f1-score']:.3f}")
	print("="*60 + "\n")
	
	return result


if __name__ == "__main__":
	result = train_level_classifier()
	print(json.dumps({k: v for k, v in result.items() if k != 'detailed_report'}, indent=2))


