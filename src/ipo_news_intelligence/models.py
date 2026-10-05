"""Core data models for IPO News Intelligence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class NewsItem:
    """Normalized news item independent of a specific feed provider."""

    title: str
    link: str
    source: str | None = None
    summary: str | None = None
    published_at: datetime | None = None
    guid: str | None = None


@dataclass(slots=True)
class Entity:
    """Company or organization that may be referenced by a news item."""

    name: str
    aliases: tuple[str, ...] = field(default_factory=tuple)
    ticker: str | None = None
    isin: str | None = None


@dataclass(slots=True)
class MatchResult:
    """Explainable entity match result."""

    entity: Entity | None
    score: float
    matched_alias: str | None = None
    evidence: tuple[str, ...] = field(default_factory=tuple)
