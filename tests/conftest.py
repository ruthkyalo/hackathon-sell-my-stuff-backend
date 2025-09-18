import os
import pytest
from fastapi.testclient import TestClient
from sell_my_stuff.main import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def test_client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_image_base64():
    """Sample base64 encoded image for testing."""
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
