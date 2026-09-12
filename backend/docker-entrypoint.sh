#!/bin/sh
set -e

# Copy baked DB to a writable path (SQLite needs journal writes).
mkdir -p /var/data
if [ -f /app/data/zomato.db ] && [ ! -f /var/data/zomato.db ]; then
  cp /app/data/zomato.db /var/data/zomato.db
fi
export DATABASE_URL=sqlite:////var/data/zomato.db

PORT="${PORT:-10000}"
echo "Starting API on 0.0.0.0:${PORT} (database: ${DATABASE_URL})"
exec uvicorn phase2.app.main:app --host 0.0.0.0 --port "$PORT" --workers 1
