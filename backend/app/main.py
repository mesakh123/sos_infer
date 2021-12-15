from fastapi import FastAPI
from .config.database import database
from .event import eventrouter

app = FastAPI(docs_url=None, redoc_url=None)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)