import sqlalchemy
from backend.app.config.database import metadata

EventTable = sqlalchemy.Table(
    "Event",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("payload_length", sqlalchemy.String),
    sqlalchemy.Column("timestamps", sqlalchemy.String),
    sqlalchemy.Column("ip_address", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.Integer),
    sqlalchemy.Column("sent", sqlalchemy.Integer),
)