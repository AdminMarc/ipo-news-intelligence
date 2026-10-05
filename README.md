# IPO News Intelligence

Open-source toolkit for collecting, deduplicating and matching IPO-related news to companies and entities.

> **Status:** early-stage / pre-alpha. The public API may change while the first stable data model and matching rules are developed.

## Why this project exists

IPO and pre-IPO news is fragmented across company blogs, financial media, exchange notices, regional publications and RSS/Atom feeds. The same story is often republished under different URLs and company names can appear through aliases, abbreviations or tickers.

IPO News Intelligence provides small, explainable Python building blocks for turning those inputs into normalized records that are easier to process downstream.

## Current capabilities

- RSS 2.0 and Atom parsing with a dependency-light standard-library implementation
- deterministic URL and GUID based deduplication
- company and alias matching
- transparent confidence scoring
- typed data models for normalized news items and match results
- unit tests for the first core behaviors

## Installation

The package is not published to PyPI yet. For development:

```bash
git clone https://github.com/AdminMarc/ipo-news-intelligence.git
cd ipo-news-intelligence
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Quick example

```python
from ipo_news_intelligence import Entity, NewsItem, confidence_score, match_entity

article = NewsItem(
    title="Acme prepares for a possible IPO",
    link="https://example.com/acme",
)

entities = [
    Entity(name="Acme Holdings", aliases=("Acme",), ticker="ACME"),
]

match = match_entity(article, entities)
score = confidence_score(
    entity_match=match.score,
    source_quality=0.8,
    ipo_context=0.9,
)

print(match.entity.name if match.entity else None)
print(score)
```

## Design principles

1. **Explainable over magical** - matching and scoring should expose why a result was produced.
2. **Deterministic by default** - the core should work without an LLM or paid API.
3. **Small public surface** - generic infrastructure belongs here; product-specific commercial logic does not.
4. **No investment advice** - this project organizes public information. It does not generate buy/sell recommendations.

## Project boundaries

This repository intentionally does **not** contain private API keys, proprietary source lists, customer data, commercial dashboard logic, or closed-source product code.

See [ROADMAP.md](ROADMAP.md) for planned work and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT. See [LICENSE](LICENSE).
