from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class User:
	user_id: str
	name: str
	email: str | None = None
	target_level: str = "B1"
	created_at: datetime = field(default_factory=datetime.utcnow)
	updated_at: datetime = field(default_factory=datetime.utcnow)

