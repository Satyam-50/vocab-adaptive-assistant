from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ProgressRecord:
	user_id: str
	texts_processed: int = 0
	words_learned: int = 0
	average_level: str = "B1"
	streak_days: int = 0
	last_active_at: datetime = field(default_factory=datetime.utcnow)

