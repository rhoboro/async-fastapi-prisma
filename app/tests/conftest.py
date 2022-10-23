from typing import Generator

import pytest
from httpx import AsyncClient

from app.main import app
from app.settings import Settings

settings = Settings()


@pytest.fixture
async def ac() -> Generator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c
