import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.middleware.ip_rate_limit import rate_limit

# Create a separate test app
test_app = FastAPI(title="Test FastAPI App")

# Apply only the middleware you want to test
test_app.middleware("http")(rate_limit)

# Dummy route for testing rate limiting
@test_app.get("/test")
async def test_endpoint():
    return {"message": "ok"}