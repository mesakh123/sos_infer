
from ..dto.eventschema import EventQuery
from ..models.eventmodels import Events
from ..config.database import engine
from ..dto.eventschema import EventSchema, EventQuery,EventPartialSchema,CreateEventSchema

from fastapi import HTTPException, Response, status
from typing import Optional

from sqlmodel import Session
import datetime
import pytz


from ..models.eventmodels import Events
from ..config.database import database


class EventService:
    async def getAllEvent(req: Optional[EventQuery] = None,skip: int = 0,limit: int = 100):

        query = Events.select()

        # Check Whether there is query request
        # If there is no request, return whole database dataset
        if not req:
            data = await database.fetch_all(query.offset(skip).limit(limit))
            return data

        # If there is query request        
        # first, convert request to dict
        req = req.dict() 
        
        # filter empty query parameters
        filtered_req = {k: v for k, v in \
                req.items() if v is not None}
        
        # Create WHERE conditions
        for attribute, value in filtered_req.items():
            query = query.where(getattr(Events.columns, attribute) == value)
        
        # Execute query
        data = await database.fetch_one(query)

        # If data doesn't exist return None
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Event not found",
                headers={"X-Error": f"Event doens't exists"}
            )
        return EventQuery(**data).dict()
        

  

    async def deleteEvent(id: int):
        try:
            query = Events.delete().where(Events.columns.id == id)
        except:
            raise HTTPException(
                status_code=404,
                detail="Event not found",
                headers={"X-Error": f"Event doens't exists"}
            )
        try:
            await database.execute(query=query)
            return Response(content="Event deleted", status_code=status.HTTP_200_OK)
        except:
            raise HTTPException(
                status_code=400,
                detail="Server Busy",
                headers={"X-Error": f"Delete error, please try again"}
            )



    async def createEvent(request: EventSchema):
        ip_address = str(request.ip_address)
        request_type = str(request.type)
        request_sent = str(request.sent)
        timestamps = str(datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S'))
        # Calculate payload length (fixed format)
        payload_length = "%05d" % (5 + 4 + len(timestamps) \
            + len(ip_address) + len(request_type))

        # Initiate Event data
        db_cr = CreateEventSchema(
            payload_length = payload_length,
            timestamps = timestamps,
            ip_address = ip_address,
            type = int(request_type),
            sent = int(request_sent),
        )
        # filter Event data
        query = {k : v for k,v in db_cr.dict().items() if v is not None}

        # Initiate Insert command
        query = Events.insert(values=query)

        # Execute data

        try:
            await database.execute(query=query)
            return Response(content="Event created", status_code=status.HTTP_200_OK)
        except:
            raise HTTPException(
                status_code=400,
                detail="Server Busy",
                headers={"X-Error": f"Create event error, please try again"}
            )



    async def updateEvent(id: int, request: EventPartialSchema):
        # Get data from database with id
        query = Events.select().where(Events.columns.id == id)
        row = await database.fetch_one(query=query)

        # If data doesn't exist
        if not row:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
                headers={"X-Error": f"Request asked for event id: [{id}]"}
            )

        # filter None request
        req = request.dict()
        filtered_req = {k: v for k, v in req.items() if v is not None}
        
        # Calculate new data length
        total = 0
        for k, v in row.items():
            if k not in filtered_req:
                total += len(str(v))
            else:
                total += len(str(filtered_req[k]))
        
        filtered_req['payload_length'] = "%05d" % (total + 4 - len(str(row['sent'])) - len(str(row['id'])))

        # Initiate UPDATE command
        query = Events.update().where(Events.columns.id == id).values(**filtered_req)
        
        # Execute Command
        try:
            await database.execute(query=query)
            return Response(content="Event updated", status_code=status.HTTP_200_OK)
        except:
            raise HTTPException(
                status_code=400,
                detail="Server Busy",
                headers={"X-Error": f"Update event error, please try again"}
            )
