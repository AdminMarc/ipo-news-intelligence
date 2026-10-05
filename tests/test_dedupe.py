from ipo_news_intelligence.dedupe import dedupe_items, normalize_url
from ipo_news_intelligence.models import NewsItem


def test_tracking_parameters_do_not_create_duplicates():
    items = [
        NewsItem(title="Example", link="https://example.com/story?utm_source=x&id=1"),
        NewsItem(title="Example", link="https://example.com/story?id=1"),
    ]

    assert len(dedupe_items(items)) == 1


def test_url_normalization_sorts_query_parameters():
    assert normalize_url("https://EXAMPLE.com/story?b=2&a=1") == (
        "https://example.com/story?a=1&b=2"
    )
