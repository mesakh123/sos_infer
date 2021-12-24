from fastapi import FastAPI, BackgroundTasks
from .config.database import database, init_db
from .event import eventrouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .event.eventrouter import EventService
from .dto.eventschema import EventSchema
from .models.eventmodels import Events
import os
import socket
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
        data = {
            'payload_length' : strings[0],
            'timestamps' : strings[1],
            "ip_address" : strings[2],
            "type" : int(strings[3])
        }
        event = EventSchema(**data)
        attemps = 5
        
        saved = False
        while attemps:
            try:
                
                last_record_id = await EventService.webSocketCreateEvent(event)
                writer.write(request.encode('utf8'))
                await writer.drain()

                saved = True
                
            except:
                attemps -= 1
                
            if saved:
                break
            
            await asyncio.sleep(1)
        
        if not saved:
            raise Exception
    except: 
        writer.write(b"Please try again")
        await writer.drain()
    
    writer.close()


async def run_server():
    port = int(str(os.environ.get('TRITON_SOCKET_PORT', '9999')))
    server = await asyncio.start_server(receive_data, '0.0.0.0', port)    
    async with server:
        await asyncio.gather(server.serve_forever()) 


async def run_client(ip, port):
    
    while True:
        reader, writer = await asyncio.open_connection(ip , port, ssl=False)
        query = Events.select().where(Events.c.sent == 0)
        data = await database.fetch_all(query=query)
        if data:
            for d in data:
                new_data = dict(d.items())
                new_data.pop("sent")
                id = new_data['id']
                new_data.pop("id")
                s= ";".join(str(v) for k,v in new_data.items()) +";"
                new_data['sent'] = 1
                query = Events.update().where(Events.c.id == int(id)).values(**new_data)
                sent = False
                await database.execute(query=query)
                writer.write(s.encode("utf-8"))
                
        writer.close()
        await writer.wait_closed()
            
async def run_client2(ip, port):
    
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(ip,port)
            query = Events.select().where(Events.c.sent == 0)
            data = await database.fetch_all(query=query)
            if data:
                for d in data:
                    new_data = dict(d.items())
                    new_data.pop("sent")
                    id = new_data['id']
                    new_data.pop("id")
                    string= ";".join(str(v) for k,v in new_data.items()) +";"
                    new_data['sent'] = 1
                    query = Events.update().where(Events.c.id == int(id)).values(**new_data)
                    sent = False
                    await database.execute(query=query)
                    s.send(string.encode("utf-8"))
            await asyncio.sleep(3)

async def tcp_reconnect():
    host = str(os.environ.get('FE_SOCKET_IP', '0.0.0.0'))
    port = int(str(os.environ.get('FE_SOCKET_PORT', '5001')))
    server = '{} {}'.format(host, port)
    while True:
        print('Connecting to server {} ...'.format(server))
        try:
            await run_client2(host, port)
        except ConnectionRefusedError:
            print('Connection to server {} failed!'.format(server))
        except asyncio.TimeoutError:
            print('Connection to server {} timed out!'.format(server))
        else:
            print('Connection to server {} is closed.'.format(server))
        await asyncio.sleep(2.0)

@app.on_event("startup")
async def startup():
    #asyncio.create_task()
    await init_db()
    await database.connect()
    app.state._db = database
    asyncio.create_task(run_server())
    asyncio.create_task(tcp_reconnect())
    

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    for task in asyncio.Task.all_tasks():
        task.cancel()   

@app.get("/")
async def Hello():
    return "Hello"


app.include_router(eventrouter.router)