"""Dependency-light RSS and Atom parsing."""

from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from .models import NewsItem


def _text(element: ET.Element | None, tag: str) -> str:
    if element is None:
        return ""
    child = element.find(tag)
    return (child.text or "").strip() if child is not None and child.text else ""


def _parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None


def parse_feed(xml_text: str, source_url: str | None = None) -> list[NewsItem]:
    """Parse basic RSS 2.0 or Atom feed XML into normalized news items."""

    root = ET.fromstring(xml_text)
    items: list[NewsItem] = []

    if root.tag.endswith("rss") or root.find("channel") is not None:
        channel = root.find("channel")
        if channel is None:
            return items
        source = _text(channel, "title") or source_url
        for node in channel.findall("item"):
            items.append(
                NewsItem(
                    title=_text(node, "title"),
                    link=_text(node, "link"),
                    source=source,
                    summary=_text(node, "description") or None,
                    published_at=_parse_date(_text(node, "pubDate")),
                    guid=_text(node, "guid") or None,
                )
            )
        return items

    # Atom namespaces are usually default namespaces, so use suffix matching.
    def child_text(node: ET.Element, suffix: str) -> str:
        for child in node:
            if child.tag.endswith(suffix):
                return (child.text or "").strip()
        return ""

    feed_title = child_text(root, "title") or source_url
    for entry in [node for node in root if node.tag.endswith("entry")]:
        link = ""
        for child in entry:
            if child.tag.endswith("link"):
                link = (child.attrib.get("href") or child.text or "").strip()
                if link:
                    break
        published = child_text(entry, "published") or child_text(entry, "updated")
        items.append(
            NewsItem(
                title=child_text(entry, "title"),
                link=link,
                source=feed_title,
                summary=child_text(entry, "summary") or child_text(entry, "content") or None,
                published_at=_parse_date(published),
                guid=child_text(entry, "id") or None,
            )
        )

    return items


def fetch_feed(url: str, timeout: float = 10.0) -> list[NewsItem]:
    """Fetch and parse a public RSS or Atom feed."""

    request = Request(url, headers={"User-Agent": "ipo-news-intelligence/0.1"})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        charset = response.headers.get_content_charset() or "utf-8"
        xml_text = response.read().decode(charset, errors="replace")
    return parse_feed(xml_text, source_url=url)
