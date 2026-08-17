FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

WORKDIR /app

# System deps for building wheels (some packages need a compiler on slim images)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Persistent directory for the SQLite database
RUN mkdir -p /app/data && chown -R nobody:nogroup /app
USER nobody

ENV DB_DIR=/app/data

EXPOSE 5000

# Use gunicorn for production. 2 workers is plenty for an IO-bound LLM chat app.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
