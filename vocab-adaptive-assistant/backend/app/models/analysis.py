from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class VocabularyEntry:
    word: str
    meaning: str
    synonyms: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AnalysisResult:
    level: str
    simplified_text: str
    difficult_words: list[VocabularyEntry] = field(default_factory=list)
