import pytest

from ipo_news_intelligence.scoring import confidence_score


def test_confidence_score_is_weighted_and_bounded():
    assert confidence_score(
        entity_match=1.0,
        source_quality=0.5,
        ipo_context=0.5,
    ) == 0.8


def test_confidence_score_rejects_invalid_values():
    with pytest.raises(ValueError):
        confidence_score(entity_match=1.1)
