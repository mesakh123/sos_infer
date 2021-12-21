from typing import Optional
from fastapi import APIRouter, WebSocket,  Cookie, Depends, FastAPI, Query, WebSocket, status
from ..dto.eventschema import EventSchema
from ..event.eventrouter import EventService

router = APIRouter(prefix="/ws", tags=["Web Socket"])


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            event = EventSchema(**data)
            query = await EventService.webSocketCreateEvent(event)
            if query is None:
                raise Exception
            result = ";".join(str(v) for k,v in query.items())
            await websocket.send_text(result)
        except: 
            await websocket.send_text("Please try again")