FROM postgres
RUN SQL_FILE="ls -latr ./postgres-data/daily/ | tail -1"
ADD $SQL_FILE /docker-entrypoint-initdb.d