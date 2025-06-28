import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app.main import app

@pytest.fixture(scope="module")
def client():
    """Provides a reusable FastAPI TestClient for all tests."""
    return TestClient(app)
