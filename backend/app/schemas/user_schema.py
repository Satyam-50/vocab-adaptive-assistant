from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
	name: str = Field(..., min_length=2, max_length=100)
	email: EmailStr | None = None
	target_level: str = Field(default="B1")


class UserResponse(BaseModel):
	user_id: str
	name: str
	email: EmailStr | None = None
	target_level: str
	created_at: datetime
	updated_at: datetime

