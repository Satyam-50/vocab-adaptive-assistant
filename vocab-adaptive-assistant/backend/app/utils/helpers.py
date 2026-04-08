from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any


def load_pickle_artifact(path: Path) -> Any:
	with path.open("rb") as file_handle:
		return pickle.load(file_handle)


def preserve_case(source: str, replacement: str) -> str:
	if source.isupper():
		return replacement.upper()
	if source[:1].isupper():
		return replacement[:1].upper() + replacement[1:]
	return replacement


def deduplicate_by_key(items: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
	seen: set[Any] = set()
	unique_items: list[dict[str, Any]] = []
	for item in items:
		value = item.get(key)
		if value in seen:
			continue
		seen.add(value)
		unique_items.append(item)
	return unique_items

