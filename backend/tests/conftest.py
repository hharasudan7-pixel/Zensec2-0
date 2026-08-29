"""Shared pytest fixtures for the ZentraSec backend test suite.

Provides:
    client      – a synchronous TestClient wrapping the FastAPI app.
    mock_gemini – patches Gemini model.generate_content so tests never hit the live API.
"""
import sys
import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Ensure the backend directory (parent of tests/) is on the Python path so
# `import main` and `import services.copilot` resolve correctly.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """A session-scoped synchronous HTTP test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def mock_gemini():
    """Patch services.copilot.model.generate_content so tests receive
    a mocked response without hitting the live Gemini API.

    Yields the mock object so individual tests can adjust return values or
    raise specific exceptions.
    """
    fake_response = MagicMock()
    fake_response.text = "Mocked copilot answer"

    with patch("services.copilot.model.generate_content") as mock_generate:
        mock_generate.return_value = fake_response
        yield mock_generate
