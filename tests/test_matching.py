from ipo_news_intelligence.matching import match_entity
from ipo_news_intelligence.models import Entity, NewsItem


def test_title_alias_match_is_strong():
    item = NewsItem(
        title="Acme prepares for a possible IPO",
        link="https://example.com/acme",
    )
    entity = Entity(name="Acme Holdings", aliases=("Acme",))

    result = match_entity(item, [entity])

    assert result.entity == entity
    assert result.matched_alias == "Acme"
    assert result.score >= 0.75
    assert "alias_in_title" in result.evidence
