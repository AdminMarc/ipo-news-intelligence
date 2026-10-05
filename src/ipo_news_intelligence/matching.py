"""Transparent company and alias matching."""

from __future__ import annotations

import re

from .models import Entity, MatchResult, NewsItem


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[\w]+", text.casefold(), flags=re.UNICODE))


def _contains_phrase(text: str, phrase: str) -> bool:
    """Return True when a normalized phrase appears on token boundaries."""

    if not phrase:
        return False
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) is not None


def match_entity(item: NewsItem, entities: list[Entity]) -> MatchResult:
    """Match a news item to the strongest exact name or alias occurrence.

    The initial implementation deliberately favors explainability over fuzzy
    heuristics. Scores are deterministic and based on where the match occurs.
    """

    title = _normalize(item.title)
    body = _normalize(item.summary or "")

    best = MatchResult(entity=None, score=0.0)

    for entity in entities:
        candidates = (entity.name, *entity.aliases)
        for alias in candidates:
            normalized_alias = _normalize(alias)
            if not normalized_alias:
                continue

            score = 0.0
            evidence: list[str] = []

            if _contains_phrase(title, normalized_alias):
                score += 0.75
                evidence.append("alias_in_title")

            if _contains_phrase(body, normalized_alias):
                score += 0.20
                evidence.append("alias_in_summary")

            if entity.ticker and _contains_phrase(
                f"{title} {body}",
                _normalize(entity.ticker),
            ):
                score += 0.05
                evidence.append("ticker_match")

            score = min(score, 1.0)
            if score > best.score:
                best = MatchResult(
                    entity=entity,
                    score=score,
                    matched_alias=alias,
                    evidence=tuple(evidence),
                )

    return best
