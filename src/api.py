import sys
import os
import pickle
import numpy as np
import hdbscan
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from mask_pii import mask_text
from urgency_score import hybrid_urgency_score
from sentence_transformers import SentenceTransformer
from pathlib import Path

load_dotenv()
API_KEY = os.getenv("API_KEY")

bearer_scheme = HTTPBearer()

def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

# Load cached clusterer and centroids
CACHE_PATH = Path("cache/cluster_cache.pkl")
if CACHE_PATH.exists():
    cache = pickle.loads(CACHE_PATH.read_bytes())
    centroids = cache["centroids"]
    cluster_ids = cache["cluster_ids"]
else:
    centroids = np.empty((0,))  # fallback empty
    cluster_ids = []

def assign_cluster(embedding: np.ndarray) -> int:
    if centroids.size == 0:
        return -1
    # compute L2 distances
    dists = np.linalg.norm(centroids - embedding, axis=1)
    idx = int(np.argmin(dists))
    # ensure Python int
    return int(cluster_ids[idx])

app = FastAPI(title="AI Support Triage API", version="1.0.0")

# Load model once
bert_model = SentenceTransformer("all-MiniLM-L6-v2")
clusterer = hdbscan.HDBSCAN(min_cluster_size=2)

# Define request model
class TicketInput(BaseModel):
    subject: str
    body: str
    lang: str = "en"

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post(
    "/analyze-ticket",
    dependencies=[Security(verify_api_key)]
)
def analyze_ticket(ticket: TicketInput):
    # Anonymize
    combined = f"{ticket.subject} {ticket.body}"
    masked_text = mask_text(combined, lang=ticket.lang)

    # Embed
    embedding = bert_model.encode([masked_text])[0]

    # Cluster
    cluster_label = assign_cluster(embedding)

    # Score urgency
    t = {"ticket_id": "API", "subject": ticket.subject, "body": ticket.body}
    scored = hybrid_urgency_score(t)

    return {
        "urgency_score": scored["urgency_score"],
        "urgency_reason": scored["urgency_reason"],
        "cluster_id": cluster_label
    }
