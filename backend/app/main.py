from fastapi import FastAPI, Websocket
from .config.database import database
from .event import eventrouter,eventservice
from .dto import eventschema
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            event = eventschema.EventSchema(**data)
            query = await eventservice.EventService.webSocketCreateEvent(event)
            if query is None:
                raise Exception
            result = ";".join(str(v) for k,v in query.items())
            await websocket.send_text(result)
        except: 
            await websocket.send_text("Please try again")
        
        

app.include_router(eventrouter.router)