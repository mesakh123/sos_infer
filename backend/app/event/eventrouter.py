from typing import Optional
from fastapi import APIRouter
from backend.app.dto.eventschema import EventQuery, EventSchema
from .eventservice import EventService

router = APIRouter(prefix="/event", tags=["Events"])


@router.get('/')
def GetAllEvent(id: Optional[int] = None,timestamps: Optional[str]= None,
    ip_address: Optional[str]= None, type: Optional[int]= None, sent: Optional[int]= None):
    if id or timestamps or ip_address or type:
        request = {}
        if id:
            request.update({'id':id})
        if timestamps:
            request.update({'timestamps':timestamps})
        if ip_address:
            request.update({'ip_address':ip_address})
        if type:
            request.update({'type':type})
        if sent:
            request.update({'sent':sent})
        request = EventQuery(**request)
        return EventService.getAllEvent(request) 
    return EventService.getAllEvent()

@router.post("/")
def createEvent(event: EventSchema):
    return EventService.createEvent(event)


@router.post("/{id}")
def updateEvent(id: int, request: EventSchema):
    return EventService.updateEvent(id=id, request=request)


@router.delete("/{id}")
def deleteEvent(id: int):
    return EventService.deleteEvent(id=id)