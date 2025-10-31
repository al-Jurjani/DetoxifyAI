# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files (not just app/)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install pytest

# Make sure Python can find the app package
ENV PYTHONPATH=/app

# Expose app port
EXPOSE 8000

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
