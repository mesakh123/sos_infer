from typing import Optional
from fastapi import APIRouter, WebSocket,  Cookie, Query, WebSocket, status
from ..dto.eventschema import EventSchema
from ..event.eventrouter import EventService
import websockets
import json
router = APIRouter(prefix="/ws", tags=["Web Socket"])


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/ws2")
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
    

@router.websocket("/ws")
async def websocket_endpoint():
    
    uri = "ws://localhost:5001/"
    
    while True:
        data = await websockets.receive_json()
        data = json.loads(data)
        try:
            event = EventSchema(**data)
            query = await EventService.webSocketCreateEvent(event)
            if query is None:
                raise Exception
            result = ";".join(str(v) for k,v in query.items()) +";"            
            await websockets.send_text(result)
        except: 
            await websockets.send_text("Please try again")