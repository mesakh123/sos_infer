
import sqlalchemy
import os, urllib
from databases import Database

#SQLALCHAMY_DATABASE_URL = "sqlite:///./event.db"
#engine = create_engine(SQLALCHAMY_DATABASE_URL, echo=True)



db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'dev')
db_port = urllib.parse.quote_plus(str(os.environ.get('DB_PORT', '5432')))
db_user = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_USER', 'root')))
db_pass = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_PASSWORD', 'linkernetworks')))
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
