# Flask blog application image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (including migrations for `flask db upgrade`)
COPY . .

# The SQLite database file lives in /app/data; persist it via a volume.
# Note: a VOLUME must be a directory, so the DB file is placed inside it.
ENV DB_DATABASE=data/flaskblog.db
VOLUME ["/app/data"]

EXPOSE 5000

# Apply database migrations, then start the production WSGI server
ENV FLASK_APP=app.py
CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 --workers 2 app:app"]
