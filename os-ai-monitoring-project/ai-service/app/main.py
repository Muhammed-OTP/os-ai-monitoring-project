from __future__ import annotations

import os
import time
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram
from prometheus_client import make_asgi_app
from prometheus_client import ProcessCollector, PlatformCollector

from .model import TinySentimentModel


# --- Prometheus metrics ---
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of HTTP requests",
    ["endpoint", "method", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint", "method"],
)
INPROGRESS = Gauge(
    "api_inprogress_requests",
    "Number of in-progress HTTP requests",
)
INFERENCE_LATENCY = Histogram(
    "model_inference_latency_seconds",
    "Model inference latency in seconds",
)

# Collect basic process and platform metrics (CPU time, memory RSS, etc.)
# In some environments these collectors may already be registered.
for collector in (ProcessCollector, PlatformCollector):
    try:
        collector()
    except ValueError:
        # Duplicated timeseries - already registered.
        pass


class PredictIn(BaseModel):
    text: str


class PredictOut(BaseModel):
    label: str
    score: float
    model: str


app = FastAPI(title="AI Model API (with Prometheus metrics)")
model = TinySentimentModel()


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method

    start = time.perf_counter()
    INPROGRESS.inc()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        elapsed = time.perf_counter() - start
        INPROGRESS.dec()
        REQUEST_LATENCY.labels(endpoint=endpoint, method=method).observe(elapsed)
        REQUEST_COUNT.labels(endpoint=endpoint, method=method, http_status=str(status_code)).inc()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text must not be empty")

    t0 = time.perf_counter()
    pred = model.predict(text)
    INFERENCE_LATENCY.observe(time.perf_counter() - t0)

    return PredictOut(label=pred.label, score=pred.score, model="tfidf+logreg")


# Expose Prometheus metrics at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
