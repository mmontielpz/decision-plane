FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY scripts ./scripts

# Create canonical data directory for SQLite
RUN mkdir -p /app/backend/data/db

# Canonical database path (matches local + tests)
ENV DATABASE_PATH=/app/backend/data/db/metadata.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
