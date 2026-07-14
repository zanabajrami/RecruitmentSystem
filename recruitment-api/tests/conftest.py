import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """
    Creates a clean test client instance to execute HTTP requests 
    against the FastAPI application without running the live server.
    """
    with TestClient(app) as c:
        yield c