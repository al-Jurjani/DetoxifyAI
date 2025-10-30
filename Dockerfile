# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY ./app /app

# Install runtime + dev dependencies
# (fastapi, uvicorn, prometheus-client, ruff, black, pytest, pytest-cov, requests)
RUN pip install --no-cache-dir \
    fastapi uvicorn prometheus-client \
    ruff black pytest pytest-cov requests

# Expose app port (must match CI CANARY_PORT)
EXPOSE 8000

# Add a simple healthcheck (used in CI canary step)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
