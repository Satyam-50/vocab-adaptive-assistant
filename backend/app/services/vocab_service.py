"""
Advanced NLP Pipeline for Vocabulary Analysis
Vocabulary Level Adaptive Reading Assistant

Features:
- Intelligent text preprocessing (tokenization, lemmatization, stemming)
- CEFR-aware difficult word detection
- Production-quality word frequency analysis (wordfreq library)
- Real WordNet-based synonyms and definitions
- Semantic text simplification
- Caching and logging
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from pathlib import Path

import joblib
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from wordfreq import zipf_frequency

from backend.app.core.constants import CEFR_LEVELS, COMMON_WORDS, MAX_DIFFICULT_WORDS
from backend.app.models.analysis import VocabularyEntry
from backend.app.utils.readability import estimate_level_from_readability
from backend.app.utils.tokenizer import split_sentences, tokenize_words, unique_preserve_order


# ============================================================================
# LOGGING & CONFIGURATION (Define first, before usage)
# ============================================================================

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Constants for word difficulty detection
WORD_MIN_LENGTH = 5  # Ignore shorter words (too common)
FREQUENCY_VERY_DIFFICULT = 3.5  # Zipf frequency threshold for very difficult
FREQUENCY_DIFFICULT = 4.5  # Zipf frequency threshold for difficult


# ============================================================================
# SETUP: Download required NLTK data
# ============================================================================

def _ensure_nltk_data() -> None:
	"""Download NLTK data if not already present."""
	required_data = [
		('tokenizers/punkt', 'punkt'),
		('corpora/stopwords', 'stopwords'),
		('corpora/wordnet', 'wordnet'),
	]
	
	for data_path, data_name in required_data:
		try:
			nltk.data.find(data_path)
		except LookupError:
			try:
				nltk.download(data_name, quiet=True)
			except Exception as e:
				logger.warning(f"Could not download NLTK data '{data_name}': {e}")


_ensure_nltk_data()


# Try to load stopwords, use fallback if not available
try:
	STOPWORDS_EN = set(stopwords.words('english'))
except Exception as e:
	logger.warning(f"NLTK stopwords not available ({e}), using fallback")
	STOPWORDS_EN = COMMON_WORDS


# ============================================================================
# TEXT PREPROCESSING MODULE
# ============================================================================

class TextPreprocessor:
	"""Advanced text preprocessing with lemmatization and normalization."""
	
	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.stop_words = STOPWORDS_EN
	
	@staticmethod
	def normalize(text: str) -> str:
		"""Normalize text: remove extra whitespace, lowercase."""
		text = (text or "").strip()
		text = re.sub(r'\s+', ' ', text)
		return text
	
	def tokenize(self, text: str) -> list[str]:
		"""
		Tokenize text into words using NLTK.
		Removes punctuation and filters empty tokens.
		"""
		try:
			tokens = word_tokenize(self.normalize(text))
			return [t for t in tokens if re.match(r'^[a-zA-Z]+$', t)]
		except Exception as e:
			logger.warning(f"Tokenization error: {e}")
			return tokenize_words(text)
	
	def lemmatize(self, token: str) -> str:
		"""Lemmatize token using WordNet lemmatizer."""
		try:
			return self.lemmatizer.lemmatize(token.lower())
		except Exception as e:
			logger.warning(f"Lemmatization error for '{token}': {e}")
			return token.lower()
	
	def preprocess(self, text: str) -> dict:
		"""
		Full preprocessing pipeline.
		
		Returns:
			dict with keys:
			- normalized_text: cleaned text
			- sentences: list of sentences
			- tokens: list of words
			- lemmas: list of lemmatized words
		"""
		normalized = self.normalize(text)
		sentences = split_sentences(normalized)
		tokens = self.tokenize(normalized)
		lemmas = [self.lemmatize(token) for token in tokens]
		
		return {
			"normalized_text": normalized,
			"sentences": sentences,
			"tokens": tokens,
			"lemmas": lemmas,
		}


# ============================================================================
# CEFR LEVEL CLASSIFICATION MODULE
# ============================================================================

class CEFRClassifier:
	"""
	CEFR level classification using:
	- Trained ML model (if available)
	- Fallback heuristic (readability-based)
	"""
	
	CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
	DEFAULT_LEVEL = "B1"
	
	def __init__(self, model_path: Path | str | None = None):
		self.model = None
		self.vectorizer = None
		self.fallback_enabled = True
		
		if model_path:
			self._load_model(model_path)
	
	def _load_model(self, model_dir: Path | str) -> None:
		"""Load trained classifier and vectorizer from disk."""
		model_dir = Path(model_dir)
		clf_path = model_dir / "level_classifier.pkl"
		vec_path = model_dir / "vectorizer.pkl"
		
		try:
			if clf_path.exists() and vec_path.exists():
				self.model = joblib.load(clf_path)
				self.vectorizer = joblib.load(vec_path)
				logger.info("✓ Loaded trained CEFR classifier model")
			else:
				logger.warning(f"Model files not found at {model_dir}")
		except Exception as e:
			logger.warning(f"Failed to load model: {e}. Using fallback heuristic.")
	
	def predict(self, text: str) -> str:
		"""
		Predict CEFR level using ML model (if available) or heuristic.
		
		Args:
			text: Input text to classify
		
		Returns:
			CEFR level string (A1-C2)
		"""
		if not text or not text.strip():
			return self.DEFAULT_LEVEL
		
		# Try ML model first
		if self.model and self.vectorizer:
			try:
				features = self.vectorizer.transform([text])
				prediction = self.model.predict(features)[0]
				
				if prediction in self.CEFR_LEVELS:
					logger.debug(f"ML prediction: {prediction}")
					return prediction
			except Exception as e:
				logger.warning(f"ML prediction failed: {e}")
		
		# Fallback to heuristic
		level = estimate_level_from_readability(text)
		logger.debug(f"Heuristic prediction: {level}")
		return level


# ============================================================================
# WORD FREQUENCY & DIFFICULTY ANALYSIS
# ============================================================================

class WordDifficultyAnalyzer:
	"""
	Analyze word difficulty using:
	- Zipf frequency (wordfreq library)
	- Stopword filtering
	- Word length heuristics
	- CEFR-aware thresholds
	"""
	
	def __init__(self):
		self.preprocessor = TextPreprocessor()
		self.min_word_length = WORD_MIN_LENGTH
		self.frequency_very_difficult = FREQUENCY_VERY_DIFFICULT
		self.frequency_difficult = FREQUENCY_DIFFICULT
	
	@lru_cache(maxsize=1024)
	def get_frequency(self, word: str, lang: str = "en") -> float:
		"""
		Get Zipf frequency of a word.
		Higher = more common (max ~8)
		Lower = more rare (min ~1)
		
		Cached for performance.
		"""
		try:
			freq = zipf_frequency(word.lower(), lang)
			return freq if freq is not None else 0.0
		except Exception as e:
			logger.debug(f"Frequency lookup failed for '{word}': {e}")
			return 0.0
	
	def is_difficult(self, word: str, text_level: str) -> bool:
		"""
		Determine if a word is difficult relative to text level.
		
		Logic:
		- Filter stopwords (too common)
		- Filter short words (< 5 chars)
		- Check frequency threshold
		- Adjust threshold based on text CEFR level
		"""
		word_lower = word.lower()
		
		# Skip common/basic words
		if word_lower in COMMON_WORDS or word_lower in stopwords.words('english'):
			return False
		
		# Skip short words
		if len(word) < self.min_word_length:
			return False
		
		# Get word frequency
		freq = self.get_frequency(word_lower)
		
		# Adaptive threshold based on text level
		if text_level in ("A1", "A2"):
			threshold = self.frequency_difficult
		elif text_level in ("B1", "B2"):
			threshold = self.frequency_difficult - 0.5
		else:  # C1, C2
			threshold = self.frequency_very_difficult
		
		# Word is difficult if frequency is below threshold
		return freq < threshold
	
	def rank_by_difficulty(self, words: list[str], text_level: str) -> list[tuple[str, float]]:
		"""
		Rank words by difficulty score.
		Returns list of (word, difficulty_score) sorted by score descending.
		"""
		results = []
		for word in words:
			if self.is_difficult(word, text_level):
				freq = self.get_frequency(word.lower())
				# Difficulty score = inverse of frequency (lower freq = higher difficulty)
				difficulty_score = max(10 - freq, 0) if freq > 0 else 10
				results.append((word, difficulty_score))
		
		# Sort by difficulty score (descending)
		return sorted(results, key=lambda x: x[1], reverse=True)


# ============================================================================
# WORD MEANINGS & SYNONYMS (WordNet-based)
# ============================================================================

class WordNetLookup:
	"""
	Get word meanings and synonyms using NLTK WordNet.
	Production-quality semantic information.
	"""
	
	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
	
	@lru_cache(maxsize=512)
	def get_wordnet_synsets(self, word: str) -> list[str]:
		"""Get synset definitions (meanings) for a word."""
		try:
			synsets = wordnet.synsets(word.lower())
			if synsets:
				definitions = [synset.definition() for synset in synsets]
				return definitions[:3]  # Top 3 definitions
		except Exception as e:
			logger.debug(f"WordNet lookup failed for '{word}': {e}")
		return []
	
	@lru_cache(maxsize=512)
	def get_wordnet_synonyms(self, word: str) -> list[str]:
		"""Get synonyms for a word using WordNet."""
		try:
			synonyms = set()
			synsets = wordnet.synsets(word.lower())
			
			if synsets:
				for synset in synsets:
					for lemma in synset.lemmas():
						synonym = lemma.name().replace('_', ' ')
						if synonym.lower() != word.lower():
							synonyms.add(synonym)
				
				# Return top 5 most frequent synonyms
				return sorted(list(synonyms), key=len)[:5]
		except Exception as e:
			logger.debug(f"Synonym lookup failed for '{word}': {e}")
		return []
	
	def get_meaning(self, word: str) -> str | None:
		"""
		Get the primary meaning of a word.
		Returns first definition or None.
		"""
		definitions = self.get_wordnet_synsets(word)
		if definitions:
			return definitions[0][:100] + "..." if len(definitions[0]) > 100 else definitions[0]
		return None
	
	def get_synonyms(self, word: str) -> list[str]:
		"""Get synonyms for a word."""
		return self.get_wordnet_synonyms(word)


# ============================================================================
# TEXT SIMPLIFICATION MODULE
# ============================================================================

class TextSimplifier:
	"""
	Simplify text by replacing difficult words with simpler alternatives.
	Uses WordNet to find simpler synonyms.
	"""
	
	def __init__(self):
		self.wordnet_lookup = WordNetLookup()
		self.difficulty_analyzer = WordDifficultyAnalyzer()
	
	@staticmethod
	def _find_simplest_synonym(synonyms: list[str]) -> str | None:
		"""
		Select the simplest synonym based on:
		- Word length (shorter = simpler)
		- Frequency (more common = simpler)
		"""
		if not synonyms:
			return None
		
		# Sort by length first (shorter words are simpler)
		sorted_syns = sorted(synonyms, key=lambda w: (len(w), zipf_frequency(w, 'en')))
		return sorted_syns[0]
	
	def simplify(self, text: str, difficult_words: list[str]) -> str:
		"""
		Replace difficult words with simpler synonyms.
		
		Args:
			text: Original text
			difficult_words: List of words to simplify
		
		Returns:
			Simplified text
		"""
		simplified = text
		replacement_count = 0
		
		for word in difficult_words:
			synonyms = self.wordnet_lookup.get_synonyms(word)
			simpler = self._find_simplest_synonym(synonyms)
			
			if simpler and simpler.lower() != word.lower():
				# Case-insensitive replacement
				pattern = re.compile(re.escape(word), re.IGNORECASE)
				simplified = pattern.sub(simpler, simplified)
				replacement_count += 1
				
				if replacement_count >= 5:  # Limit replacements to keep text coherent
					break
		
		logger.info(f"Simplified {replacement_count} words")
		return simplified


# ============================================================================
# MAIN VOCABULARY SERVICE (PRODUCTION PIPELINE)
# ============================================================================

class VocabularyService:
	"""
	Complete vocabulary analysis pipeline.
	Orchestrates all components for intelligent word analysis.
	"""
	
	def __init__(self, model_dir: Path | str | None = None):
		self.preprocessor = TextPreprocessor()
		self.classifier = CEFRClassifier(model_dir)
		self.difficulty_analyzer = WordDifficultyAnalyzer()
		self.wordnet_lookup = WordNetLookup()
		self.simplifier = TextSimplifier()
	
	def extract_difficult_words(self, text: str, max_words: int = MAX_DIFFICULT_WORDS) -> list[VocabularyEntry]:
		"""
		Extract and rank difficult words from text.
		
		Args:
			text: Input text
			max_words: Maximum number of words to return
		
		Returns:
			List of VocabularyEntry objects with meaning and synonyms
		"""
		if not text or not text.strip():
			return []
		
		try:
			# Detect text level
			level = self.classifier.predict(text)
			
			# Preprocess
			preprocessed = self.preprocessor.preprocess(text)
			tokens = preprocessed["tokens"]
			
			# Rank by difficulty
			ranked = self.difficulty_analyzer.rank_by_difficulty(tokens, level)
			
			# Keep unique words only
			seen = set()
			entries = []
			
			for word, difficulty_score in ranked:
				word_lower = word.lower()
				if word_lower in seen or len(entries) >= max_words:
					continue
				
				seen.add(word_lower)
				
				# Build vocabulary entry
				entry = VocabularyEntry(
					word=word,
					meaning=self._get_meaning_for_word(word),
					synonyms=self._get_synonyms_for_word(word)
				)
				entries.append(entry)
			
			logger.info(f"Extracted {len(entries)} difficult words from text")
			return entries
		
		except Exception as e:
			logger.error(f"Error extracting difficult words: {e}")
			return []
	
	def _get_meaning_for_word(self, word: str) -> str:
		"""Get meaning from WordNet or fallback."""
		meaning = self.wordnet_lookup.get_meaning(word)
		if meaning:
			return meaning
		return f"An advanced word: {word}"
	
	def _get_synonyms_for_word(self, word: str) -> list[str]:
		"""Get synonyms from WordNet or fallback."""
		synonyms = self.wordnet_lookup.get_synonyms(word)
		if synonyms:
			return synonyms
		
		# Fallback: generate placeholder synonyms
		base = word.rstrip("s") or word
		return [f"{base}", f"similar to {base}"]
	
	def process_text(self, text: str) -> dict:
		"""
		Complete pipeline: preprocess → classify → analyze → simplify.
		
		Returns:
			{
				"level": "B2",
				"simplified_text": "...",
				"difficult_words": [
					{
						"word": "proliferation",
						"meaning": "rapid increase",
						"synonyms": ["growth", "expansion"]
					}
				],
				"metadata": {
					"word_count": 150,
					"sentence_count": 8,
					"complexity_score": 6.5
				}
			}
		"""
		if not text or not text.strip():
			return {
				"level": self.classifier.DEFAULT_LEVEL,
				"simplified_text": "",
				"difficult_words": [],
				"metadata": {}
			}
		
		try:
			# 1. Preprocess
			preprocessed = self.preprocessor.preprocess(text)
			
			# 2. Classify level
			level = self.classifier.predict(preprocessed["normalized_text"])
			
			# 3. Extract difficult words
			difficult_words = self.extract_difficult_words(text)
			difficult_word_list = [dw.word for dw in difficult_words]
			
			# 4. Simplify text
			simplified = self.simplifier.simplify(text, difficult_word_list)
			
			# 5. Gather metadata
			metadata = {
				"word_count": len(preprocessed["tokens"]),
				"sentence_count": len(preprocessed["sentences"]),
				"complexity_score": round(len(difficult_word_list) / max(len(preprocessed["tokens"]), 1) * 10, 2),
			}
			
			result = {
				"level": level,
				"simplified_text": simplified,
				"difficult_words": [
					{
						"word": entry.word,
						"meaning": entry.meaning,
						"synonyms": entry.synonyms
					}
					for entry in difficult_words
				],
				"metadata": metadata
			}
			
			logger.info(f"✓ Processed text: level={level}, difficult_words={len(difficult_words)}")
			return result
		
		except Exception as e:
			logger.error(f"Error in text processing pipeline: {e}")
			return {
				"level": self.classifier.DEFAULT_LEVEL,
				"simplified_text": text,
				"difficult_words": [],
				"metadata": {"error": str(e)}
			}
	
	def get_replacement_map(self) -> dict[str, str]:
		"""Get word replacement map for text simplification."""
		replacement_map = {}
		for synsets in wordnet.all_synsets():
			for lemma in synsets.lemmas():
				word = lemma.name().replace('_', ' ')
				synonyms = self.wordnet_lookup.get_synonyms(word)
				if synonyms:
					replacement_map[word] = synonyms[0]
		return replacement_map
	
	def replacement_map(self) -> dict[str, str]:
		"""Backward compatibility wrapper for get_replacement_map()."""
		return self.get_replacement_map()

