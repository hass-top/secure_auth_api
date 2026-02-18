import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app   # ← use REAL app

# --------------------------
# Sample test user
# --------------------------

TEST_USER = {
    "name": "TESadapuaoezarajeaefT",
    "email": "teradaaaffzepadsahofedreat@example.com",
    "password": "StrongPass123!",
    "verificationpassword": "StrongPass123!"
}

ACCESS_TOKEN = None


# --------------------------
# RATE LIMIT TEST (async)
# --------------------------

@pytest.mark.asyncio
async def test_rate_limit():
    async with AsyncClient(app=app, base_url="http://test") as client:

        # Hit endpoint multiple times
        for _ in range(10):
            response = await client.get("/test")
            assert response.status_code == 200

        # Next request should be blocked
        response = await client.get("/test")
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests"


# --------------------------
# SYNC CLIENT FOR AUTH TESTS
# --------------------------

client = TestClient(app)


@pytest.fixture(scope="module")
def register_user():
    response = client.post("/auth/register", json=TEST_USER)
    assert response.status_code in (200, 201)
    return TEST_USER


def test_register(register_user):
    assert register_user["email"] == TEST_USER["email"]


def test_login(register_user):
    global ACCESS_TOKEN

    response = client.post("/auth/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
  
    assert data["token_type"] == "bearer"

    ACCESS_TOKEN = data["access_token"]
  
    print("ACCESS_TOKEN:", ACCESS_TOKEN)
  


def test_logout():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = client.post("/auth/logout", headers=headers)
    print("LOGOUT RESPONSE:", response.status_code, response.text)

    assert response.status_code == 200
    assert "message" in response.json()



def test_logout():
    global ACCESS_TOKEN
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",  # put token in header
        "Content-Type": "application/json"
    }

    response = client.post("/auth/logout", headers=headers)
    print("LOGOUT RESPONSE:", response.status_code, response.text)

    assert response.status_code == 200
    assert "message" in response.json()
