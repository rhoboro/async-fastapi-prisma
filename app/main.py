from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import database
from app.api.main import router as api_router
from app.settings import Settings

settings = Settings()
app = FastAPI(title="async-fastapi-prisma")
app.include_router(api_router, prefix="/api")

try:
    from app.graphql.main import router as graphql_router

    app.include_router(graphql_router)
except ModuleNotFoundError:
    pass


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
