https://github.com/vincedgy/fastapi-async-with-postgresql

https://vincedgy.github.io/fastapi-async-with-postgresql/

https://fastapi.tiangolo.com/advanced/async-sql-databases/

https://www.tutlinks.com/fastapi-with-postgresql-crud-async/

https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08


https://www.jeffastor.com/blog/pairing-a-postgresql-db-with-your-dockerized-fastapi-app

A. Start alembic
0. sudo docker-compose build
1. pip3 install alembic
2. alembic init alembic
3. then , change data in env.py and alembic.ini
4. docker-compose run app alembic revision --autogenerate -m "New Migration"
5. docker-compose run app alembic upgrade head
6. sudo docker-compose up --build -d --force-recreate
