"""Manage terminology records and similarity lookups."""

from . import db_utils


def save_term(term: dict) -> None:
    """Persist a terminology entry."""
    db_utils.save_json_record('terminology.json', term)
