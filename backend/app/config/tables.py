import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EventTableBase(Base):
    __tablename__ = "events"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    payload_length = sqlalchemy.Column(sqlalchemy.String)
    timestamps = sqlalchemy.Column(sqlalchemy.String)
    ip_address = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    sent = sqlalchemy.Column(sqlalchemy.Integer)
