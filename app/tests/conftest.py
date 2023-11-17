from typing import Generator

import pytest
from httpx import AsyncClient

from app import database
from app.main import app
from app.settings import Settings

settings = Settings()


@pytest.fixture(scope="function", autouse=True)
async def db() -> Generator:
    await database.connect()
    try:
        async with database._db.tx() as tx:
            yield tx
            raise ValueError()
    except ValueError:
        pass
    finally:
        await database.disconnect()


@pytest.fixture
async def ac() -> Generator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c
