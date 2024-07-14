# MQTT Logging

This client tool can be used to log incoming MQTT messages to a Postgres database. It uses Python with the paho package to work with MQTT and psycopg2 to connect to the Postgres database.

* Python 3.9 (Slim)
* python-dotenv (\~=1.0) paho-mqtt (\~=2.1) and psycopg2-binary (\~=2.9)
* Postgres 16
* Docker (tested with Docker Engine 27.0)

## Features

* .env file for credentials to connect to the MQTT broker and for the Postgres database
* Logs connections, subscriptions, messages and other client logs (such as PINGREQ and PINGRESP)
* Postgres database is persisted in the Postgres directory
* Automatically creates the table in Postgres on first startup
* Postgres health check

## Working with Docker

Before the first start, you need to specify an `.env` file. See `.env.example` file for the necessary credentials you need to specify. Then run the command `docker compose build` (or `docker compose build --no-cache` if you have run it before).

Then start the containers by running `docker compose up -w` in the terminal. When the `client.py` file is saved, the client container is restarted to incorporate the changes.

You can stop the containers with the command `docker compose down`.

## Known Issues / Limitations

* Better error handling on client side
* Log more issues on client side
* Make client configuration more robust (e.g authentication)
