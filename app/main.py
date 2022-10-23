from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import database
from app.api.main import router as api_router
from app.settings import Settings

settings = Settings()
app = FastAPI(title="async-fastapi-prisma")
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
