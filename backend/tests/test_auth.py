import uuid

def test_signup(client):
    email = f"test+{uuid.uuid4().hex[:6]}@example.com"
    response = client.post("/auth/signup", json={
        "email": email,
        "password": "test1234",
        "full_name": "Tester"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_login(client):
    email = f"test+{uuid.uuid4().hex[:6]}@example.com"
    password = "test1234"

    # Create user
    client.post("/auth/signup", json={
        "email": email,
        "password": password,
        "full_name": "Tester"
    })

    # Login
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("LOGIN RESPONSE:", response.status_code, response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()
