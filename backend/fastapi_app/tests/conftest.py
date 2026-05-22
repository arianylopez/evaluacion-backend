import pytest
import os
from httpx import AsyncClient, ASGITransport
from app.main import app

os.environ["TESTING"] = "True"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client