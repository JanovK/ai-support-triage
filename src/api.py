import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from mask_pii import mask_text
from urgency_score import hybrid_urgency_score
from sentence_transformers import SentenceTransformer
import hdbscan

load_dotenv()
API_KEY = os.getenv("API_KEY")

bearer_scheme = HTTPBearer()

def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

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
    # 1) Anonymize
    combined = f"{ticket.subject} {ticket.body}"
    masked_text = mask_text(combined, lang=ticket.lang)

    # 2) Embed
    embedding = bert_model.encode([masked_text])[0]

    # 3) Cluster (stubbed as -1 for single-ticket API)
    cluster_label = -1

    # 4) Score urgency
    t = {"ticket_id": "API", "subject": ticket.subject, "body": ticket.body}
    scored = hybrid_urgency_score(t)

    return {
        "urgency_score": scored["urgency_score"],
        "urgency_reason": scored["urgency_reason"],
        "cluster_id": cluster_label
    }
