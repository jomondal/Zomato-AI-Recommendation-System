#!/bin/sh
set -e

mkdir -p /app/data

PORT="${PORT:-8000}"
exec uvicorn phase2.app.main:app --host 0.0.0.0 --port "$PORT" --workers 1
