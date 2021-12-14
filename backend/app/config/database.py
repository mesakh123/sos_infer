
import sqlalchemy
import os, urllib
from databases import Database

#SQLALCHAMY_DATABASE_URL = "sqlite:///./event.db"
#engine = create_engine(SQLALCHAMY_DATABASE_URL, echo=True)



db_host = os.environ.get('db_host', 'localhost')
db_name = os.environ.get('db_name', 'dev')
db_port = urllib.parse.quote_plus(str(os.environ.get('db_port', '5432')))
db_user = urllib.parse.quote_plus(str(os.environ.get('db_user', 'root')))
db_pass = urllib.parse.quote_plus(str(os.environ.get('db_pass', 'linkernetworks')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))
db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

database: Database = Database(db_url,
                    #ssl=True,
                    min_size=5,
                    max_size=20)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    #DATABASE_URL, connect_args={"check_same_thread": False}
    db_url
)
metadata.create_all(engine)
