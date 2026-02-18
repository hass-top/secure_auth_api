import pytest 
from httpx import AsyncClient 
from main import app

@pytest.mark.asyncio 
async def test_rate_limit ( ): 
    async with AsyncClient ( app= app , base_url="http;//testserver") as client :
        for i in range ( 10 ) : 
            response = await client.get("/test")
            assert response.status_code == 200 
            json_data = response.json()
            assert "message" in json_data
            assert json_data["message"] == "ok"

        response = await client.get("/test")
        json_data = response.json()
        assert json_data.get("detail") == "Too many requests"