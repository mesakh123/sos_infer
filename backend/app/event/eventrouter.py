from typing import Optional
from fastapi import APIRouter
from ..dto.eventschema import EventQuery, EventSchema, EventPartialSchema
from .eventservice import EventService

router = APIRouter(prefix="/event", tags=["Events"])


@router.get('/')
async def GetAllEvent(id: Optional[int] = None,timestamps: Optional[str]= None,
    ip_address: Optional[str]= None, type: Optional[int]= None, sent: Optional[int]= None,
    skip: int = 0,
    limit: int = 100,
    ):
    if id is not None or timestamps is not None  or ip_address is not None  or type is not None :
        request = {}
        if id is not None :
            request.update({'id':id})            
        if timestamps is not None :
            request.update({'timestamps':timestamps})
        if ip_address is not None :
            request.update({'ip_address':ip_address})
        if type is not None :
            request.update({'type':type})
        if sent is not None :
            request.update({'sent':sent})
        request = EventQuery(**request)
        return await EventService.getAllEvent(request, skip = skip, limit = limit) 
    return await EventService.getAllEvent(skip = skip, limit = limit)

@router.post("/")
async def createEvent(event: EventSchema):
    return await EventService.createEvent(event)


@router.post("/{id}")
async def updateEvent(id: int, request: EventPartialSchema):
    return await EventService.updateEvent(id=id, request=request)


@router.delete("/{id}")
async def deleteEvent(id: int):
    return await EventService.deleteEvent(id=id)