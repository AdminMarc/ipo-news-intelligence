# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-10-05

Initial public development release.

### Added

- RSS 2.0 and Atom parsing
- normalized news-item, entity, and match-result data models
- deterministic GUID and URL based deduplication
- company and alias matching with explainable evidence
- weighted confidence scoring
- unit tests for feed parsing, deduplication, matching, and scoring
- GitHub Actions test workflow for Python 3.11 and 3.12
- project roadmap, contribution guide, security policy, and MIT license

### Fixed

- prevent short aliases from matching inside unrelated words by enforcing token boundaries

### Notes

This is an early development release. The public API may change before a stable 1.0 release.
