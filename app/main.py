from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from pydantic import BaseModel
import joblib
import re
import string
import os

app = FastAPI(title="DetoxifyAI API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "app_request_count", "Total number of requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency (seconds)", ["endpoint"]
)

# Model globals
model = None
vectorizer = None
model_loaded = False

# Preprocessing function
def preprocess_aggressive(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[0-9]+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    return text

@app.on_event("startup")
async def load_model():
    global model, vectorizer, model_loaded

    # Get the project root directory (parent of app folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    model_path = os.path.join(project_root, "MLFlow", "experiments", "model.pkl")
    vectorizer_path = os.path.join(project_root, "MLFlow", "experiments", "tfidf.pkl")

    print(f"[INFO] Looking for model at: {model_path}")
    print(f"[INFO] Looking for vectorizer at: {vectorizer_path}")

    try:
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            model_loaded = True
            print("[SUCCESS] Model and vectorizer loaded successfully!")
        else:
            print("[WARNING] Model files not found. Running in mock mode.")
            print(f"[WARNING] Model exists: {os.path.exists(model_path)}")
            print(f"[WARNING] Vectorizer exists: {os.path.exists(vectorizer_path)}")
            model_loaded = False
    except Exception as e:
        print(f"[ERROR] Failed to load model: {str(e)}")
        model_loaded = False

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
    return {
        "message": "DetoxifyAI API running successfully",
        "model_loaded": model_loaded
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class Query(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_loaded}


@app.post("/predict")
async def predict(req: Query):
    if not req.text or req.text.strip() == "":
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Mock response if model not loaded
    if not model_loaded or model is None or vectorizer is None:
        return {
            "input": req.text,
            "prediction": "non-toxic",
            "confidence": 0.50,
            "model_loaded": False,
            "note": "Using mock prediction - model not loaded"
        }

    try:
        # Real prediction
        preprocessed = preprocess_aggressive(req.text)
        X = vectorizer.transform([preprocessed])
        prediction = model.predict(X)[0]
        probability = float(model.predict_proba(X)[0, 1])

        return {
            "input": req.text,
            "prediction": "toxic" if prediction == 1 else "non-toxic",
            "confidence": probability if prediction == 1 else (1 - probability),
            "toxic_probability": probability,
            "model_loaded": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
