from fastapi import FastAPI
from .config.database import database
from .event import eventrouter
from .websocket import websocketrouter
from fastapi.middleware.cors import CORSMiddleware

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
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)
app.include_router(websocketrouter.router)