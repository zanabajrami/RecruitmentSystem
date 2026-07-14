def test_health_check(client):
    """
    Test that the root endpoint returns a 200 OK and healthy status.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "project" in response.json()