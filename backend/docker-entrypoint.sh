#!/bin/sh
set -e

mkdir -p /app/data

if [ ! -f /app/data/zomato.db ]; then
  echo "Database not found. Starting background Hugging Face ingestion..."
  (
    python phase1/scripts/ingest_hf_dataset.py --clear
    python phase1/scripts/validate_data.py
    echo "Background ingestion finished."
  ) &
fi

PORT="${PORT:-8000}"
exec uvicorn phase2.app.main:app --host 0.0.0.0 --port "$PORT"
