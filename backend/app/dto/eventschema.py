from pydantic import BaseModel
from typing import Optional


class EventSchema(BaseModel):
    timestamps: str
    ip_address: str
    type: int
    class Config():
        #enable orm_mode
        orm_mode = True

    
class EventQuery(BaseModel):
    id: Optional[int]
    timestamps: Optional[str]
    ip_address: Optional[str]
    type: Optional[int]
    sent: Optional[int]
    class Config():
        #enable orm_mode
        orm_mode = True