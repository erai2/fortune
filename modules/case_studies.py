"""Case study data utilities."""

from . import db_utils


def save_case(study: dict) -> None:
    """Persist a case study record."""
    db_utils.save_json_record('case_studies.json', study)
