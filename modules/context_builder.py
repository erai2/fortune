"""Construct prompts by injecting related context."""

from typing import List


def build_prompt(question: str, contexts: List[str]) -> str:
    """Combine a question with context passages."""
    joined = "\n".join(contexts)
    return f"{joined}\n\nQ: {question}\nA:"
