import logging
from typing import Annotated, AsyncIterator

from fastapi import Depends

from app.prisma import Prisma, errors
from app.settings import settings

logger = logging.getLogger(__name__)
_db = Prisma(
    auto_register=True,
    datasource={"url": settings.DATABASE_URL},
)


async def connect() -> None:
    await _db.connect()


async def disconnect() -> None:
    await _db.disconnect()


async def get_db() -> AsyncIterator[Prisma]:
    try:
        yield _db
    except errors.PrismaError as e:
        logger.exception(f"{e!r}")


Database = Annotated[Prisma, Depends(get_db)]
