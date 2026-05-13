import copy

import pytest
from fastapi.testclient import TestClient
from src.app import activities, app


initial_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities before each test."""
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    yield


@pytest.fixture
def client():
    """Test client fixture for FastAPI app."""
    return TestClient(app)