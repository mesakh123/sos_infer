from fastapi import FastAPI, BackgroundTasks
from .config.database import database, init_db
from .event import eventrouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .socket import socketrouter


dev = True

if dev:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # asyncio.create_task()
    await init_db()
    await database.connect()
    app.state._db = database
    asyncio.create_task(socketrouter.run_server())
    asyncio.create_task(socketrouter.tcp_reconnect())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    for task in asyncio.Task.all_tasks():
        task.cancel()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)
