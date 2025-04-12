def test_dashboard(auth_client):
    response = auth_client.get("user/dashboard")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # or your actual expected structure
