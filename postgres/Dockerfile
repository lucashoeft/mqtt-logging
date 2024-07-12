FROM postgres:16

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y wget build-essential postgresql-server-dev-16

COPY ./init.sql /docker-entrypoint-initdb.d/