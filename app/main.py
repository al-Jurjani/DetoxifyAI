from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from pydantic import BaseModel

app = FastAPI(title="DetoxifyAI API")

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "app_request_count", "Total number of requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency (seconds)", ["endpoint"]
)


@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(latency)
    return response


@app.get("/")
def read_root():
    return {"message": "DetoxifyAI API running successfully 🚀"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class Query(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(req: Query):
    # Stub logic — always returns fake "toxic" label
    text = req.text
    return {"input": text, "prediction": "non-toxic", "confidence": 0.99}
