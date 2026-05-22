import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/api/v1/healthz")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_get_table_types(async_client):
    response = await async_client.get("/api/v1/tables/types/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_menu_missing_date(async_client):
    response = await async_client.get("/api/v1/menu/")
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["loc"] == ["query", "date"]
    assert error_detail["msg"] == "Field required"

@pytest.mark.asyncio
async def test_check_availability_missing_party(async_client):
    response = await async_client.get(
        "/api/v1/reservations/availability/?date=2026-05-23&time=20:00&tz=UTC"
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_rate_limiter_exceeded(async_client):
    for _ in range(60):
        res = await async_client.get("/api/v1/healthz")
        assert res.status_code in [200, 429]

    response_blocked = await async_client.get("/api/v1/healthz")
    assert response_blocked.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert response_blocked.json()["detail"] == "Too Many Requests - Rate limit exceeded"