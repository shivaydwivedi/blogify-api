#!/bin/sh
set -eu

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

python <<'PY'
import os
import time

import psycopg

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
dbname = os.environ.get("POSTGRES_DB", "blogify")
user = os.environ.get("POSTGRES_USER", "blogify")
password = os.environ.get("POSTGRES_PASSWORD", "blogify")

deadline = time.monotonic() + 60
last_error = None

while time.monotonic() < deadline:
    try:
        with psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=3,
        ):
            print("PostgreSQL is reachable.")
            break
    except psycopg.OperationalError as exc:
        last_error = exc
        print("Waiting for PostgreSQL...")
        time.sleep(2)
else:
    raise SystemExit(f"PostgreSQL did not become reachable: {last_error}")
PY

python manage.py migrate --noinput
python manage.py check

exec python manage.py runserver 0.0.0.0:8000
