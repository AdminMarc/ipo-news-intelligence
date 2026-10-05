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


def test_short_alias_does_not_match_inside_other_word():
    item = NewsItem(
        title="Paid subscriptions rise before earnings",
        link="https://example.com/story",
    )
    entity = Entity(name="Artificial Intelligence Corp", aliases=("AI",))

    result = match_entity(item, [entity])

    assert result.entity is None
    assert result.score == 0.0


def test_multiword_alias_matches_on_phrase_boundaries():
    item = NewsItem(
        title="Acme Labs files confidential IPO paperwork",
        link="https://example.com/acme-labs",
    )
    entity = Entity(name="Acme Holdings", aliases=("Acme Labs",))

    result = match_entity(item, [entity])

    assert result.entity == entity
    assert result.matched_alias == "Acme Labs"
