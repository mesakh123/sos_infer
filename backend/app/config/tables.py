import sqlalchemy
from .database import metadata
from sqlalchemy.ext.declarative import declarative_base

EVENT_ID_SEQ = sqlalchemy.Sequence('event_id_seq')

Base = declarative_base()

class EventTableBase(Base):
    __tablename__ = "events"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    payload_length = sqlalchemy.Column(sqlalchemy.String)
    timestamps = sqlalchemy.Column(sqlalchemy.String,)
    ip_address = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    sent = sqlalchemy.Column(sqlalchemy.Integer)


EventTable = sqlalchemy.Table(
    "events",
    metadata,
    sqlalchemy.Column("id", primary_key=True),
    sqlalchemy.Column("payload_length", sqlalchemy.String),
    sqlalchemy.Column("timestamps", sqlalchemy.String),
    sqlalchemy.Column("ip_address", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.Integer),
    sqlalchemy.Column("sent", sqlalchemy.Integer),
)