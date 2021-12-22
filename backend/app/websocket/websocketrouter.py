from typing import Optional
from fastapi import APIRouter, WebSocket,  Cookie, Query, WebSocket, status
from ..dto.eventschema import EventSchema
from ..event.eventrouter import EventService
from ..models.eventmodels import Events
from ..config.database import database
import websockets
import asyncio
from ..main import app
from starlette.websockets import WebSocketDisconnect
router = APIRouter(prefix="/websocket", tags=["Web Socket"])


uri = "ws://localhost:9000/"


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

  
@database.transaction()
async def forward(ws_a: WebSocket):
    while True:
        recv_data = await ws_a.receive_text()
        print("recv data ",recv_data)
        strings = recv_data.split(";")
        data = {
            'payload_length' : strings[0],
            'timestamps' : strings[1],
            "ip_address" : strings[2],
            "type" : strings[3]
        }
        
        event = EventSchema(**data)
        last_record_id = await EventService.webSocketCreateEvent(event)
        query = Events.select().where(Events.columns.id == last_record_id)
        
        try:
            attemps = 5
            
            sent = False
            while attemps:
                await ws_a.send_text(recv_data)
                data.update({'sent':1})
                query = query.values(**data)
                try:
                    await database.execute(query=query)
                    sent = True
                except:
                    attemps -= 1
                    
                if sent: break
                await asyncio.sleep(5)
            
            if not sent:
                raise Exception
        except: 
            await ws_a.send_text("Please try again")



@app.websocket("/ws")     
async def websocket_endpoint(ws_a: WebSocket):
    
    await ws_a.accept()
    """
    async with websockets.connect(uri) as ws_b:
        fwd_task = asyncio.create_task(forward(ws_a, ws_b))
        await asyncio.gather(fwd_task)       
    """
    try:
        while True:
            send_time_task = asyncio.create_task(forward(ws_a))
            done, pending = await asyncio.wait(
                {send_time_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            for task in done:
                task.result()
    except WebSocketDisconnect:
        await ws_a.close()
    
    

@router.websocket("/w2")
async def websocket_endpoint2(fastapiwebsocket: WebSocket):
    await fastapiwebsocket.accept()
    while True:
        data = await fastapiwebsocket.receive_text()
        try:
            event = EventSchema(**data)
            query = await EventService.webSocketCreateEvent(event)
            if query is None:
                raise Exception
            result = ";".join(str(v) for k,v in query.items()) +";"            
            await fastapiwebsocket.send_text(result)
        except: 
            await fastapiwebsocket.send_text("Please try again")

@router.websocket("/w3")    
async def websocket_endpoint3(fastapiwebsocket: WebSocket):
    
    uri = "ws://localhost:5001/"
    
    while True:
        
        await asyncio.sleep(20)
        
        data = await websockets.receive_text()
        string = data.split(";")
        data = {
            'timestamps':string[1],
            "ip_address":string[2],
            "type":string[3]
        }
        
        try:
            event = EventSchema(**data)
            query = await EventService.webSocketCreateEvent(event)
            if query is None:
                raise Exception
            result = ";".join(str(v) for k,v in query.items()) +";"            
            await websockets.send_text(result)
        except: 
            await websockets.send_text("Please try again")

