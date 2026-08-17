FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

WORKDIR /app

# gcc for any wheel builds; safe to include on slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Persistent directory for the SQLite database
# Mount a volume here in production to persist data across deploys:
#   docker run -v chatty-data:/app/data ...
#   railway: it persists /app/data automatically
RUN mkdir -p /app/data
ENV DB_DIR=/app/data

# Use Railway/Docker's PORT env var if set, otherwise 5000
ENV PORT=5000

EXPOSE 5000

# Shell form so $PORT is expanded at container start.
# 2 workers, 120s timeout for slow LLM calls.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 app:app"]
