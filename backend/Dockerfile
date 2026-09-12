FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/tmp/hf
ENV DATABASE_URL=sqlite:////app/data/zomato.db

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Bake restaurant data into the image at build time (avoids OOM on free-tier runtime).
RUN mkdir -p /app/data \
    && python phase1/scripts/ingest_hf_dataset.py --clear --limit 25000

EXPOSE 8000

CMD ["sh", "./docker-entrypoint.sh"]
