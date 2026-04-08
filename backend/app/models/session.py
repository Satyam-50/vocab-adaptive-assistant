from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ReadingSession:
	session_id: str
	user_id: str
	input_length: int
	predicted_level: str
	started_at: datetime = field(default_factory=datetime.utcnow)
	ended_at: datetime | None = None

