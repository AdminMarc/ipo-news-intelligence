# Contributing

Thanks for helping improve IPO News Intelligence.

## Development setup

1. Fork and clone the repository.
2. Create a virtual environment.
3. Install the project in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

4. Run the test suite:

```bash
pytest
```

## Pull requests

Keep changes focused and explain the problem being solved. Add or update tests for behavior changes.

## Project boundaries

This repository contains generic open-source building blocks only. Please do not submit private API keys, proprietary source lists, customer data, or code copied from closed-source products.

## Code style

Prefer small, typed, dependency-light Python modules. Public functions should have docstrings and deterministic behavior where practical.
