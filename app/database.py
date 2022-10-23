import logging
from typing import AsyncIterator

from app.prisma import Prisma, errors

logger = logging.getLogger(__name__)
_db = Prisma(auto_register=True)


async def connect() -> None:
    await _db.connect()


async def disconnect() -> None:
    await _db.disconnect()


async def get_db() -> AsyncIterator[Prisma]:
    try:
        yield _db
    except errors.PrismaError as e:
        logger.exception(f"{e!r}")
