def test_login_invalid_credentials(client):
    """
    Test that the authentication endpoint returns 401 Unauthorized
    when provided with invalid user credentials using Form Data.
    """
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wronguser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401