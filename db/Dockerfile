FROM postgres:15-bullseye

ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb

RUN apt-get update

RUN apt-get update \
      && apt-get install -y curl \
      && apt-get -y install postgresql-15-pgvector \
      && apt-get -y install postgresql-15-cron

RUN mkdir -p /tmp/psql_data/

COPY structure.sql /tmp/psql_data/
COPY structure.sql /docker-entrypoint-initdb.d/