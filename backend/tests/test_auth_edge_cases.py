from fastapi.testclient import TestClient
from main import app

# Unauthorized upload should fail
def test_upload_without_token():
    unauthenticated_client = TestClient(app)  # Fresh client without login

    with open("tests/sample.pdf", "rb") as f:
        response = unauthenticated_client.post(
            "/upload-db/",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )
    assert response.status_code == 403  # or 401, depending on your HTTPBearer behavior

# Invalid or malformed JWT should be rejected
def test_upload_with_invalid_token(client):
    headers = {"Authorization": "Bearer faketoken123"}
    with open("tests/sample.pdf", "rb") as f:
        response = client.post("/upload-db/", files={"file": ("sample.pdf", f, "application/pdf")}, headers=headers)
    assert response.status_code == 401
    assert "detail" in response.json()


# Expired JWT simulation (manual token override if you’re mocking expiration logic)
def test_expired_token_behavior(monkeypatch, client):
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # example; not real
    headers = {"Authorization": f"Bearer {expired_token}"}
    
    # Normally, you would mock `decode_access_token` to raise an ExpiredSignatureError
    # For now, just assert 401 if using invalid/expired token
    response = client.get("/user/dashboard", headers=headers)
    assert response.status_code == 401


# Accessing protected dashboard without token
def test_dashboard_requires_auth():
    unauthenticated_client = TestClient(app)  # Fresh instance, no token
    response = unauthenticated_client.get("/user/dashboard")
    assert response.status_code in (403, 401)
    assert "detail" in response.json()
