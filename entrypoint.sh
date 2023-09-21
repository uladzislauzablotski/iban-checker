#! /usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:/app"

if [ "${POSTGRES_HOST}" != "localhost" ]; then
  (exec alembic --config server/alembic.ini upgrade head)
fi
poetry run python server/main.py
