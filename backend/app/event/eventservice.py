
from backend.app.dto.eventschema import EventQuery
from backend.app.models.eventmodels import Event
from backend.app.config.database import engine

from fastapi import Query

from typing import Optional

from sqlmodel import Session, and_
from backend.app.dto.eventschema import EventSchema, EventQuery


class EventService:
    def getAllEvent(req: Optional[EventQuery] = None):
        db = Session(engine)
        if req:
            #filter req
            req = req.dict()
            filtered_req = {k: v for k, v in req.items() if v is not None}
            filters = [getattr(Event, attribute) == value for attribute, value in filtered_req.items()]
            
            return db.query(Event).filter(and_(*filters)).all()

        return db.query(Event).all()

    def deleteEvent(id: int):
        db = Session(engine)
        db_id = db.query(Event).filter(Event.id == id).first()
        db.delete(db_id)
        db.commit()
        return "Delete Event"


    def createEvent(request: EventSchema):
        db = Session(engine)

        timestamps = str(request.timestamps)
        ip_address = str(request.ip_address)
        request_type = str(request.type)

        payload_length = "%05d" % (5 + 4 + len(timestamps) \
            + len(ip_address) + len(request_type))

        db_cr = Event(
            payload_length = payload_length,
            timestamps = timestamps,
            ip_address = ip_address,
            type = int(request_type),
            event = 0,
        )

        db.add(db_cr)
        db.commit()

        return "Event Created"

    def updateEvent(id: int, request: EventSchema):
        db = Session(engine)
        db_id = db.query(Event).filter(Event.id == id).first()

        timestamps = str(request.timestamps)
        ip_address = str(request.ip_address)
        request_type = str(request.type)

        db_id.timestamps = timestamps
        db_id.ip_address = ip_address
        db_id.type = request_type

        payload_length = "%05d" % (5 + 4 + len(timestamps) \
            + len(ip_address) + len(request_type))

        db_id.payload_length = payload_length

        db.commit()

        return "Update Event"

