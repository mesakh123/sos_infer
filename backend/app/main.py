from fastapi import FastAPI, BackgroundTasks
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


async def receive_data(reader, writer):

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


async def send_data(ip,port):
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip , port, ssl=False)
            query = Events.update().where(Events.columns.sent == -1)
            data = await database.fetch_all(query=query)
            for d in data:
                print(d)
        except:
            pass
        
        await asyncio.sleep(1)
        
    



async def run_server():
    port = int(str(os.environ.get('TRITON_SOCKET_PORT', '9797')))
    server = await asyncio.start_server(receive_data, '0.0.0.0', port)    
    async with server:
        await asyncio.gather(server.serve_forever()) 

async def run_client():
    ip = str(os.environ.get('FE_SOCKET_IP', '0.0.0.0'))
    port = int(str(os.environ.get('FE_SOCKET_PORT', '5001')))
    asyncio.create_task(send_data(ip,port))


@app.on_event("startup")
async def startup():
    await database.connect()
    asyncio.create_task(run_server())
    asyncio.create_task(run_client())
    

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)