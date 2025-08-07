"""Simple JSON-based persistence utilities."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def _load_json(path: Path) -> List[Any]:
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json_record(filename: str, record: dict) -> None:
    """Append a record to a JSON file under the data directory."""
    path = DATA_DIR / filename
    data = _load_json(path)
    data.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
