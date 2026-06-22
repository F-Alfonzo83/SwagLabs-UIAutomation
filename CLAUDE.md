# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI test automation suite for [SauceDemo](https://www.saucedemo.com/) using Python, Playwright, and pytest following the Page Object Model (POM) pattern.

## Commands

All commands require the virtual environment to be active: `source .venv/bin/activate`

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_login_page.py

# Run a single test by name
pytest tests/test_login_page.py::test_login_user_valid

# Run with verbose output and live logs
pytest -v -s
```

Tests run headless Firefox by default (configured in `tests/conftest.py`).

## Architecture

### Page Object Model
Each page class in `page_object_models/` receives `page` (Playwright `Page`) and `logger` in `__init__`. They define locators as instance attributes and expose three method categories:
- `should_be_open()` — asserts URL and page indicator visibility
- `should_show_critic_elements()` — asserts key interactive elements are visible
- `should_be_healthy()` — combines the above two
- Action methods (e.g., `fill_login_form`, `submit_login`) perform interactions and return the next page object when navigation occurs

### Test Session & Fixtures
`tests/conftest.py` defines a **session-scoped** `browser_instance` fixture that launches a single Firefox browser for the entire test session. All tests share one browser context and page — tests must account for shared state (the browser navigates across tests sequentially).

### Configuration
`configurations/config_loader.py` loads `configurations/config_base.yaml` at class definition time (not at instantiation). URLs are organized under `environments.testing`. Add new URL constants as methods on `ConfigLoader`.

### Logging
`utilities/logger_utility.py` exports `_logger(name)`, a factory that returns a named `logging.Logger` set to DEBUG with a stream handler. Tests import and instantiate this at module level, then pass the logger into every POM constructor.

## Adding a New Page

1. Create `page_object_models/<page_name>_page.py` with a class following the existing POM pattern.
2. Add the page URL to `configurations/config_base.yaml` and a corresponding method to `ConfigLoader`.
3. Add navigation in the preceding page's action method (returning the new page object).
4. Create `tests/test_<page_name>_page.py` using the `browser_instance` fixture.
