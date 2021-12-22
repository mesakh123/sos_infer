from fastapi import FastAPI
from .config.database import database
from .event import eventrouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .event.eventrouter import EventService
from .dto.eventschema import EventSchema
from .models.eventmodels import Events
import os

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


async def handle_client(reader, writer):

    try:
        request = (await reader.read(255)).decode('utf8')
        request = str(request)
        strings = request.split(";")
        print("Strings ",strings)
        data = {
            'payload_length' : strings[0],
            'timestamps' : strings[1],
            "ip_address" : strings[2],
            "type" : int(strings[3])
        }
        event = EventSchema(**data)
        last_record_id = await EventService.webSocketCreateEvent(event)
        attemps = 5
        
        sent = False
        while attemps:
            try:
                writer.write(request.encode('utf8'))
                await writer.drain()
                
                data.update({'sent':1})                
                query = Events.update().where(Events.columns.id == last_record_id).values(**data)
                await database.execute(query=query)
                sent = True
                
            except:
                attemps -= 1
                
            if sent: break
            await asyncio.sleep(1)
        
        if not sent:
            raise Exception
    except: 
        writer.write(b"Please try again")
        await writer.drain()
    
    writer.close()


SERVER = None
async def run_server():
    port = int(str(os.environ.get('SOCKET_PORT', '5001')))
    server = await asyncio.start_server(handle_client, '0.0.0.0', port)
    async with server:
        await server.serve_forever()    
    return server     

@app.on_event("startup")
async def startup():
    global SERVER
    await database.connect()
    SERVER = await run_server()
    

@app.on_event("shutdown")
async def shutdown():
    global SERVER    
    await database.disconnect()
    await SERVER.wait_closed()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)


