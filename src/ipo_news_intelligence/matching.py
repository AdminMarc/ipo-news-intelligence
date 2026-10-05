"""Transparent company and alias matching."""

from __future__ import annotations

import re

from .models import Entity, MatchResult, NewsItem


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[\w]+", text.casefold(), flags=re.UNICODE))


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

            if normalized_alias in title:
                score += 0.75
                evidence.append("alias_in_title")

            if normalized_alias in body:
                score += 0.20
                evidence.append("alias_in_summary")

            if entity.ticker and re.search(
                rf"(?<!\w){re.escape(entity.ticker.casefold())}(?!\w)",
                f"{title} {body}",
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
