# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app

# Expose app port (must match CI CANARY_PORT)
EXPOSE 8000

# Add a simple healthcheck (used in CI canary step)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
