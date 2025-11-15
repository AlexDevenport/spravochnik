#!/usr/bin/env bash
set -euo pipefail

export PGPASSWORD="${DB_PASS:-}"

echo "Waiting for Postgres at ${DB_HOST}:${DB_PORT}..."
RETRIES=60
COUNT=0
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}" >/dev/null 2>&1; do
  COUNT=$((COUNT+1))
  if [ $COUNT -ge $RETRIES ]; then
    echo "Postgres is still unavailable after ${RETRIES} seconds. Exiting."
    exit 1
  fi
  sleep 1
done

echo "Postgres is ready."

# -------------------------------
# Запускаем async alembic миграции
# -------------------------------
echo "Running Alembic migrations..."
alembic upgrade head

# -------------------------------
# Загружаем тестовые данные (если есть)
# -------------------------------
if [ -f /app/test_data.sql ]; then
  echo "Loading test data..."
  psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -f /app/test_data.sql || true
fi

# -------------------------------
# запускам приложение
# -------------------------------
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
