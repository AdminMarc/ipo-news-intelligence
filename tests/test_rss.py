from ipo_news_intelligence.rss import parse_feed


def test_parse_basic_rss():
    xml = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <title>Example Feed</title>
        <item>
          <title>Acme considers IPO</title>
          <link>https://example.com/acme</link>
          <guid>story-1</guid>
          <description>Acme is evaluating a public listing.</description>
        </item>
      </channel>
    </rss>
    """

    items = parse_feed(xml)

    assert len(items) == 1
    assert items[0].title == "Acme considers IPO"
    assert items[0].guid == "story-1"
