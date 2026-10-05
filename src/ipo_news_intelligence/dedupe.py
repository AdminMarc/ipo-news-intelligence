"""Deterministic duplicate detection helpers."""

from __future__ import annotations

import hashlib
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import NewsItem

_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def normalize_url(url: str) -> str:
    """Normalize a URL while removing common tracking parameters."""

    parts = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in _TRACKING_KEYS
        and not any(key.lower().startswith(prefix) for prefix in _TRACKING_PREFIXES)
    ]
    host = parts.netloc.lower()
    path = re.sub(r"/+$", "", parts.path) or "/"
    return urlunsplit((parts.scheme.lower(), host, path, urlencode(sorted(query)), ""))


def normalize_title(title: str) -> str:
    """Normalize title text for deterministic comparisons."""

    return " ".join(re.findall(r"[\w]+", title.casefold(), flags=re.UNICODE))


def item_fingerprint(item: NewsItem) -> str:
    """Return a stable content fingerprint for a news item."""

    if item.guid and item.guid.strip():
        basis = f"guid:{item.guid.strip()}"
    elif item.link and item.link.strip():
        basis = f"url:{normalize_url(item.link)}"
    else:
        basis = f"title:{normalize_title(item.title)}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def dedupe_items(items: list[NewsItem]) -> list[NewsItem]:
    """Keep the first occurrence of each deterministic fingerprint."""

    seen: set[str] = set()
    unique: list[NewsItem] = []
    for item in items:
        fingerprint = item_fingerprint(item)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        unique.append(item)
    return unique
