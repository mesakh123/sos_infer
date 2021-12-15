from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel

class Events(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    payload_length: str
    timestamps: str
    ip_address: str
    type: int
    sent: Optional[int] = 0

