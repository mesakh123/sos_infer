
import sqlalchemy
from ..config.database import metadata

Events = sqlalchemy.Table(
    "events",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("payload_length", sqlalchemy.String),
    sqlalchemy.Column("timestamps", sqlalchemy.String),
    sqlalchemy.Column("ip_address", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.Integer),
    sqlalchemy.Column("sent", sqlalchemy.Integer),
)


