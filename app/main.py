from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from pydantic import BaseModel
import joblib
import re
import string
import os
from dotenv import load_dotenv

from azure.storage.blob import BlobServiceClient
from io import BytesIO

from app.rag_pipeline import DetoxifyRAGPipeline
from app.guardrails import DetoxifyGuardrails

load_dotenv()
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
CONTAINER_NAME = "mlflow-artifacts-mlops-proj"

# Initialize blob service client as None, will be created in startup
# if connection string exists
blob_service_client = None

pipeline = None
guardrails = None

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

# NEW: Add these LLM-specific metrics
GUARDRAIL_VIOLATIONS = Counter(
    "guardrail_violations_total", "Total guardrail violations", ["rule_type"]
)

LLM_TOKENS = Counter(
    "llm_tokens_total",
    "Total tokens processed",
    ["endpoint", "token_type"],  # input/output
)

LLM_COST = Counter("llm_cost_dollars", "Estimated LLM cost in USD", ["endpoint"])

# Model globals
model = None
vectorizer = None
model_loaded = False


# Preprocessing function
def preprocess_aggressive(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[0-9]+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text


@app.on_event("startup")
async def load_model():
    global model, vectorizer, model_loaded, pipeline, guardrails

    # # Get the project root directory (parent of app folder)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # project_root = os.path.dirname(current_dir)

    # model_path = os.path.join(project_root, "MLFlow", "experiments", "model.pkl")
    # vectorizer_path = os.path.join(project_root, "MLFlow", "experiments", "tfidf.pkl")

    # print(f"[INFO] Looking for model at: {model_path}")
    # print(f"[INFO] Looking for vectorizer at: {vectorizer_path}")

    # try:
    #     if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    #         model = joblib.load(model_path)
    #         vectorizer = joblib.load(vectorizer_path)
    #         model_loaded = True
    #         print("[SUCCESS] Model and vectorizer loaded successfully!")
    #     else:
    #         print("[WARNING] Model files not found. Running in mock mode.")
    #         print(f"[WARNING] Model exists: {os.path.exists(model_path)}")
    #         print(f"[WARNING] Vectorizer exists: {os.path.exists(vectorizer_path)}")
    #         model_loaded = False
    # except Exception as e:
    #     print(f"[ERROR] Failed to load model: {str(e)}")
    #     model_loaded = False

    try:
        # Check if Azure connection string is available
        if not AZURE_CONNECTION_STRING:
            print(
                "[WARNING] No Azure connection string provided. Running in mock mode."
            )
            model_loaded = False
            return

        print(
            "[INFO] Downloading model and vectorizer from Azure Blob Storage..."
        )  # pragma: no cover

        # Create blob service client  # pragma: no cover
        global blob_service_client  # pragma: no cover
        blob_service_client = (
            BlobServiceClient.from_connection_string(  # pragma: no cover
                AZURE_CONNECTION_STRING
            )
        )

        # Blob paths (without container name prefix since it's specified separately)  # pragma: no cover
        xg_model_blob_path = "mlflow-artifacts-mlops-proj/3/4690eeee10294ed0bf0d12132887b898/artifacts/model/model.pkl"  # pragma: no cover
        xg_vectorizer_blob_path = "mlflow-artifacts-mlops-proj/3/4690eeee10294ed0bf0d12132887b898/artifacts/vectorizer/tfidf.pkl"  # pragma: no cover

        # Alternative paths for logistic regression model (commented out, using XGBoost)  # pragma: no cover
        # lg_model_blob_path = "2/b82b8de7266347c1b2dd9b52ad1d1321/artifacts/model/model.pkl"
        # lg_vectorizer_blob_path = "2/b82b8de7266347c1b2dd9b52ad1d1321/artifacts/vectorizer/tfidf.pkl"

        # Access blobs  # pragma: no cover
        model_blob = blob_service_client.get_blob_client(  # pragma: no cover
            container=CONTAINER_NAME, blob=xg_model_blob_path
        )
        vectorizer_blob = blob_service_client.get_blob_client(  # pragma: no cover
            container=CONTAINER_NAME, blob=xg_vectorizer_blob_path
        )

        # Download into memory  # pragma: no cover
        model_data = BytesIO(model_blob.download_blob().readall())  # pragma: no cover
        vectorizer_data = BytesIO(
            vectorizer_blob.download_blob().readall()
        )  # pragma: no cover

        # Load using joblib  # pragma: no cover
        model = joblib.load(model_data)  # pragma: no cover
        vectorizer = joblib.load(vectorizer_data)  # pragma: no cover

        model_loaded = True  # pragma: no cover
        print(
            "[SUCCESS] Model and vectorizer loaded successfully from Azure!"
        )  # pragma: no cover

        # Add RAG pipeline initialization
        print("[INFO] Initializing RAG pipeline...")
        # global pipeline
        pipeline = DetoxifyRAGPipeline(
            azure_connection_string=AZURE_CONNECTION_STRING,
            azure_container="detoxifyai-m2-artifacts",  # Your RAG artifacts container
        )
        print("[SUCCESS] RAG pipeline initialized!")

        print("[INFO] Initializing guardrails...")
        guardrails = DetoxifyGuardrails(
            toxicity_threshold=0.3, log_file="guardrail_events.json"
        )
        print("[SUCCESS] Guardrails initialized!")
        print(f"[DEBUG] Guardrails object: {guardrails}")
        print(f"[DEBUG] Guardrails type: {type(guardrails)}")
    except Exception as e:  # pragma: no cover
        print(f"[ERROR] Failed to load model from Azure: {str(e)}")  # pragma: no cover
        model_loaded = False  # pragma: no cover


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
        "model_loaded": model_loaded,
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
            "note": "Using mock prediction - model not loaded",
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
            "model_loaded": True,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# RAG ONLY rephase - works, but no guardrails in this
# @app.post("/rephrase")
# async def rephrase(req: Query):
#     print(f"[DEBUG] Received rephrase request: {req.text[:50]}...")

#     if not req.text or req.text.strip() == "":
#         raise HTTPException(status_code=400, detail="Text cannot be empty")

#     # Check if text is toxic first
#     print("[DEBUG] Checking toxicity...")
#     if not model_loaded or model is None or vectorizer is None:
#         print("[ERROR] ML model not loaded")
#         raise HTTPException(status_code=503, detail="ML model not loaded")

#     preprocessed = preprocess_aggressive(req.text)
#     X = vectorizer.transform([preprocessed])
#     prediction = model.predict(X)[0]

#     print(f"[DEBUG] Toxicity prediction: {prediction}")

#     if prediction == 0:
#         return {
#             "input": req.text,
#             "is_toxic": False,
#             "message": "Text is non-toxic, no rephrasing needed"
#         }

#     # Check RAG pipeline
#     print("[DEBUG] Checking RAG pipeline...")
#     if not pipeline:
#         print("[ERROR] RAG pipeline is None")
#         raise HTTPException(status_code=503, detail="RAG pipeline not available")

#     print("[DEBUG] Calling RAG pipeline...")
#     try:
#         result = pipeline.rephrase(req.text, k=5)
#         print("[DEBUG] RAG success!")
#         return {
#             "input": result['toxic_input'],
#             "is_toxic": True,
#             "rephrased": result['professional_rephrase'],
#             "retrieved_examples": result['retrieved_examples'],
#             "num_examples_used": result['num_examples_used']
#         }
#     except Exception as e:
#         print(f"[ERROR] RAG failed: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Rephrasing failed: {str(e)}")


# RAG pipeline with guardrails
@app.post("/rephrase")
async def rephrase(req: Query):
    print(f"[DEBUG] Received rephrase request: {req.text[:50]}...")

    if not req.text or req.text.strip() == "":
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # STEP 1: Input Validation (Guardrails)
    print("[DEBUG] Running input guardrails...")
    print(f"[DEBUG] Guardrails is None? {guardrails is None}")
    if not guardrails:
        print("[WARNING] Guardrails not initialized")
    else:
        print(f"[DEBUG] Calling validate_input with: {req.text[:50]}")
        valid, reason, meta = guardrails.validate_input(req.text)
        if not valid:
            print(f"[GUARDRAIL] Input blocked: {reason}")
            GUARDRAIL_VIOLATIONS.labels(rule_type=meta.get("rule", "unknown")).inc()
            return {
                "status": "blocked",
                "stage": "input",
                "reason": reason,
                "original": req.text,
                "guardrails": {
                    "input_passed": False,
                    "rule_violated": meta.get("rule"),
                    "detail": meta,
                },
            }

    # STEP 2: Check toxicity
    print("[DEBUG] Checking toxicity...")
    if not model_loaded or model is None or vectorizer is None:
        print("[ERROR] ML model not loaded")
        raise HTTPException(status_code=503, detail="ML model not loaded")

    preprocessed = preprocess_aggressive(req.text)
    X = vectorizer.transform([preprocessed])
    prediction = model.predict(X)[0]

    print(f"[DEBUG] Toxicity prediction: {prediction}")

    if prediction == 0:
        return {
            "input": req.text,
            "is_toxic": False,
            "message": "Text is non-toxic, no rephrasing needed",
            "guardrails": {"input_passed": True, "output_passed": True},
        }

    # STEP 3: RAG Rephrasing
    print("[DEBUG] Checking RAG pipeline...")
    if not pipeline:
        print("[ERROR] RAG pipeline is None")
        raise HTTPException(status_code=503, detail="RAG pipeline not available")

    print("[DEBUG] Calling RAG pipeline...")
    try:
        result = pipeline.rephrase(req.text, k=5)
        rephrased_text = result["professional_rephrase"]

        # ADD THIS - Estimate tokens (rough approximation)
        input_tokens = len(req.text.split()) * 1.3  # ~1.3 tokens per word
        output_tokens = len(rephrased_text.split()) * 1.3

        LLM_TOKENS.labels(endpoint="/rephrase", token_type="input").inc(input_tokens)
        LLM_TOKENS.labels(endpoint="/rephrase", token_type="output").inc(output_tokens)

        # Estimate cost (Mistral-7B pricing: ~$0.0002 per 1K tokens)
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * 0.0002
        LLM_COST.labels(endpoint="/rephrase").inc(cost)

        # STEP 4: Output Validation (Guardrails)
        print("[DEBUG] Running output guardrails...")
        if guardrails:
            valid, reason, meta = guardrails.validate_output(rephrased_text)
            if not valid:
                print(f"[GUARDRAIL] Output blocked: {reason}")
                GUARDRAIL_VIOLATIONS.labels(rule_type=meta.get("rule", "unknown")).inc()
                return {
                    "status": "blocked",
                    "stage": "output",
                    "reason": reason,
                    "original": req.text,
                    "attempted_rephrase": rephrased_text,
                    "guardrails": {
                        "input_passed": True,
                        "output_passed": False,
                        "rule_violated": meta.get("rule"),
                        "toxicity_score": meta.get(
                            "score", meta.get("toxicity_score", 0)
                        ),
                        "detail": meta,
                    },
                }

        # SUCCESS - All guardrails passed
        print("[DEBUG] RAG success, all guardrails passed!")
        return {
            "input": result["toxic_input"],
            "is_toxic": True,
            "rephrased": rephrased_text,
            "retrieved_examples": result["retrieved_examples"],
            "num_examples_used": result["num_examples_used"],
            "guardrails": {
                "input_passed": True,
                "output_passed": True,
                "toxicity_score": meta.get("toxicity_score", 0) if guardrails else 0,
            },
        }
    except Exception as e:
        print(f"[ERROR] RAG failed: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Rephrasing failed: {str(e)}")
