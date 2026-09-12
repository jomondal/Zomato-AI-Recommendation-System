FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000
ENV DATABASE_URL=sqlite:////var/data/zomato.db

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# Pre-built database (no Hugging Face download during deploy).
RUN mkdir -p /app/data && cp docker/zomato.db /app/data/zomato.db

EXPOSE 10000

CMD ["sh", "./docker-entrypoint.sh"]
