from fastapi import FastAPI
from backend.app.config.database import create_table

from backend.app.event import eventrouter

app = FastAPI()


@app.on_event("startup")
async def table_all():
    create_table()


@app.get("/")
def Hello():
    return "Hello"


app.include_router(eventrouter.router)