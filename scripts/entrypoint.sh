#!/bin/sh
set -eu

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

is_production() {
    [ "${DJANGO_ENVIRONMENT:-development}" = "production" ] \
        || [ "${DJANGO_SETTINGS_MODULE:-}" = "config.settings.production" ]
}

python <<'PY'
import os
import time

import psycopg

database_url = os.environ.get("DATABASE_URL")

deadline = time.monotonic() + 60
last_error = None

while time.monotonic() < deadline:
    try:
        if database_url:
            connection = psycopg.connect(database_url, connect_timeout=3)
        else:
            connection = psycopg.connect(
                host=os.environ.get("POSTGRES_HOST", "db"),
                port=int(os.environ.get("POSTGRES_PORT", "5432")),
                dbname=os.environ.get("POSTGRES_DB", "blogify"),
                user=os.environ.get("POSTGRES_USER", "blogify"),
                password=os.environ.get("POSTGRES_PASSWORD", "blogify"),
                connect_timeout=3,
            )

        with connection:
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
python manage.py bootstrap_superuser
if is_production; then
    python manage.py collectstatic --noinput
fi
python manage.py check

if is_production; then
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers="${GUNICORN_WORKERS:-2}"
fi

exec python manage.py runserver 0.0.0.0:8000
