
import sqlalchemy
import os, urllib
import nest_asyncio
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine


db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'dev')
db_port = urllib.parse.quote_plus(str(os.environ.get('DB_PORT', '5432')))
db_user = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_USER', 'root')))
db_pass = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_PASSWORD', 'linkernetworks')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))
db_header= os.environ.get('DB_HEADER',"postgresql")
db_url = f"{db_header}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

database: Database = Database(db_url,
                    #ssl=True,
                    min_size=5,
                    max_size=20)
metadata = sqlalchemy.MetaData()

engine = create_async_engine(db_url)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


import asyncio
loop = asyncio.get_event_loop()
loop.create_task(init_db())
#metadata.create_all(engine)
