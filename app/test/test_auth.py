import pytest
from fastapi.testclient import TestClient
from app.test.test_main import  test_app

client = TestClient(test_app)

# Sample user
TEST_USER = {
    "name": "TEST",
    "email": "TEST@example.com",
    "password": "cdeklje'-àç(fd4)",
    "verificationpassword": "cdeklje'-àç(fd4)"
}

@pytest.fixture(scope="module")
def register_user():
    # Register a user
    response = client.post("/auth/register", json=TEST_USER)
    assert response.status_code in (200, 201)
    return TEST_USER

def test_register(register_user):
    # Already covered in fixture
    assert register_user["email"] == TEST_USER["email"]

def test_login(register_user):
    # Login
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Save token for other tests
    global ACCESS_TOKEN
    ACCESS_TOKEN = data["access_token"]

def test_protected_route():
    # Access a protected endpoint
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.get("/test", headers=headers)
    assert response.status_code == 200
    assert response.text == '"Test OK"'  # or whatever your endpoint returns

def test_refresh_token():
    # Example if you have /auth/refresh endpoint using cookies
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_logout():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
