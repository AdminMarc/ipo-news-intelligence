"""IPO News Intelligence public package."""

from .dedupe import dedupe_items
from .matching import match_entity
from .models import Entity, MatchResult, NewsItem
from .rss import parse_feed
from .scoring import confidence_score

__all__ = [
    "Entity",
    "MatchResult",
    "NewsItem",
    "confidence_score",
    "dedupe_items",
    "match_entity",
    "parse_feed",
]

__version__ = "0.1.0"
