from pydantic import BaseModel
from typing import Optional
import datetime

class EventPartialSchema(BaseModel):
    type: Optional[int]
    sent: Optional[int] = 0
    class Config():
        #enable orm_mode
        orm_mode = True

class EventSchema(BaseModel):
    #timestamps: datetime.datetime
    ip_address: str
    type: int
    sent: Optional[int] = 0
    class Config():
        #enable orm_mode
        orm_mode = True


class CreateEventSchema(BaseModel):
    timestamps: str
    payload_length: str
    ip_address: str
    type: int
    sent: Optional[int] = 0
    class Config():
        #enable orm_mode
        orm_mode = True



    
class EventQuery(BaseModel):
    id: Optional[int]
    timestamps: Optional[datetime.datetime]
    ip_address: Optional[str]
    type: Optional[int]
    sent: Optional[int]
    class Config():
        #enable orm_mode
        orm_mode = True