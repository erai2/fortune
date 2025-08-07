"""Utilities for handling structured fortune-telling analyses."""

from . import db_utils


def save_analysis(record: dict) -> None:
    """Persist a structured analysis record using db_utils."""
    db_utils.save_json_record('suam_analysis.json', record)
