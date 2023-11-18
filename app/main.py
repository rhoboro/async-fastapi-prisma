from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import database
from app.api.main import router as api_router


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator[None, None]:
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(title="async-fastapi-prisma", lifespan=lifespan)
app.include_router(api_router, prefix="/api")

try:
    from app.graphql.main import router as graphql_router

    app.include_router(graphql_router)
except ModuleNotFoundError:
    pass


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
