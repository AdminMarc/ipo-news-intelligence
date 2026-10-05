"""Small, explainable confidence scoring utilities."""

from __future__ import annotations


def confidence_score(
    *,
    entity_match: float,
    source_quality: float = 0.5,
    ipo_context: float = 0.5,
) -> float:
    """Combine normalized signals into a transparent confidence score.

    Each input must be between 0 and 1. Entity matching is weighted highest
    because the library's primary job is assigning news to the right entity.
    """

    values = {
        "entity_match": entity_match,
        "source_quality": source_quality,
        "ipo_context": ipo_context,
    }
    for name, value in values.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")

    score = (0.60 * entity_match) + (0.20 * source_quality) + (0.20 * ipo_context)
    return round(score, 4)
