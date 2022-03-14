from fastapi import FastAPI, BackgroundTasks
from fastapi.logger import logger as fastapi_logger
from .config.database import database, init_db
from .event import eventrouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .socket import socketrouter

import logging


logging.root.handlers = []
logging.root.setLevel(logging.DEBUG)
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True


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

    curr_logger = logging.getLogger(__name__)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
        )
    )
    logging.root.addHandler(handler)


    curr_logger.info("Connect database started")
    uvicorn_access_logger.info("Connect database started")

    await init_db()
    await database.connect()
    app.state._db = database

    curr_logger.info("Connect database finished")
    uvicorn_access_logger.info("Connect database finished")

    uvicorn_access_logger.info("start socket server")
    asyncio.create_task(socketrouter.run_server())
    uvicorn_access_logger.info("start socket server finished")

    uvicorn_access_logger.info("Start  client socket")
    asyncio.create_task(socketrouter.tcp_reconnect())
    uvicorn_access_logger.info("Client socket finished")





@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    for task in asyncio.Task.all_tasks():
        task.cancel()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)
