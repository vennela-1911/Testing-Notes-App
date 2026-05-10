import pytest

pytest_plugins = [
    "fixtures.browser_fixture"
]


def pytest_configure(config):

    config.addinivalue_line(
        "markers",
        "ui: UI tests"
    )

    config.addinivalue_line(
        "markers",
        "api: API tests"
    )

    config.addinivalue_line(
        "markers",
        "e2e: End to End tests"
    )