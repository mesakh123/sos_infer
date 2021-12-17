https://github.com/vincedgy/fastapi-async-with-postgresql

https://vincedgy.github.io/fastapi-async-with-postgresql/

https://fastapi.tiangolo.com/advanced/async-sql-databases/

https://www.tutlinks.com/fastapi-with-postgresql-crud-async/

https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08


https://www.jeffastor.com/blog/pairing-a-postgresql-db-with-your-dockerized-fastapi-app

A. Start alembic
0. sudo docker-compose build
1. pip3 install alembic
2. alembic init -t async alembic
3. then , change data in env.py and alembic.ini
4. docker-compose run --rm app alembic revision --autogenerate -m "New Migration"
5. docker-compose run --rm app alembic upgrade head
6. sudo docker-compose up --build -d --force-recreate


create role root superuser;
create database sos_infer_db;
ALTER USER root with PASSWORD 'linkeradmin123';
psql postgres -d sos_infer_db

http://127.0.0.1:9000/event/?id=1&timestamps=timestamps&ip_address=127.0.0.1&type=0&sent=1&skip=100&limit=300