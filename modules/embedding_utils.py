"""Placeholder for NLP embedding utilities."""

from typing import List


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Return dummy embeddings for a list of texts."""
    return [[0.0] * 3 for _ in texts]
