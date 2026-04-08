from __future__ import annotations

import hashlib


def hash_text(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def verify_text_hash(value: str, digest: str) -> bool:
	return hash_text(value) == digest

