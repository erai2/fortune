"""Basic theory data management."""

from . import db_utils


def save_theory(entry: dict) -> None:
    """Persist a basic theory record."""
    db_utils.save_json_record('basic_theory.json', entry)
