
from ..dto.eventschema import EventQuery
from ..models.eventmodels import Events
from ..config.database import engine
from ..dto.eventschema import EventSchema, EventQuery,EventPartialSchema

from fastapi import HTTPException

from typing import Optional

from sqlmodel import Session

from ..config.tables import EventTable
from ..config.database import database


class EventService:
    async def getAllEvent(req: Optional[EventQuery] = None):
        query = EventTable.select()
        if not req:
            data = await database.fetch_all(query)
            return data

        req = req.dict()
        filtered_req = {k: v for k, v in req.items() if v is not None}
        for attribute, value in filtered_req.items():
            query = query.where(getattr(EventTable.columns, attribute) == value)
        #filters = [getattr(Event, attribute) == value for attribute, value in filtered_req.items()]

        #print("Filters ",*filters)
        data = await database.fetch_one(query)
        if not data:
            return None
        return EventQuery(**data).dict()
        
  

    async def deleteEvent(id: int):
        query = EventTable.delete().where(EventTable.columns.id == id)
        await database.execute(query=query)
        return "Event Deleted"


    async def createEvent(request: EventSchema):
        
        timestamps = str(request.timestamps)
        ip_address = str(request.ip_address)
        request_type = str(request.type)
        request_sent = str(request.sent)

        payload_length = "%05d" % (5 + 4 + len(timestamps) \
            + len(ip_address) + len(request_type))

        db_cr = Events(
            payload_length = payload_length,
            timestamps = timestamps,
            ip_address = ip_address,
            type = int(request_type),
            sent = int(request_sent),
        )
        query = {k : v for k,v in db_cr.dict().items() if v is not None}
        query = EventTable.insert(values=query)
        user_id = await database.execute(query)

        return "Event Created"

    async def updateEvent(id: int, request: EventPartialSchema):
        query = EventTable.select().where(EventTable.columns.id == id)
        row = await database.fetch_one(query=query)

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
                headers={"X-Error": f"Request asked for event id: [{id}]"}
            )

        req = request.dict()
        filtered_req = {k: v for k, v in req.items() if v is not None}
        
        total = 0
        for k, v in row.items():

            if k not in filtered_req:
                total += len(str(v))
            else:
                total += len(str(filtered_req[k]))
        filtered_req['payload_length'] = "%05d" % (total + 4 - len(str(row['sent'])) - len(str(row['id'])))
        query = EventTable.update().where(EventTable.columns.id == id).values(**filtered_req)
        
        await database.execute(query=query)


        return "Update Event"

