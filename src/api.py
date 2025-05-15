from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mask_pii import mask_text
from urgency_score import hybrid_urgency_score
from sentence_transformers import SentenceTransformer
import hdbscan

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

@app.post("/analyze-ticket")
def analyze_ticket(ticket: TicketInput):
    try:
        # Step 1: Anonymize
        combined = f"{ticket.subject} {ticket.body}"
        masked_text = mask_text(combined, lang=ticket.lang)

        # Step 2: Embedding
        embedding = bert_model.encode([masked_text])[0]

        # Step 3: Clustering (on single point returns -1)
        cluster_label = -1  # Future: batch clustering could persist state

        # Step 4: Scoring
        ticket_dict = {
            "ticket_id": "TEMP",
            "subject": ticket.subject,
            "body": ticket.body
        }
        scored = hybrid_urgency_score(ticket_dict)

        return {
            "urgency_score": scored["urgency_score"],
            "urgency_reason": scored["urgency_reason"],
            "cluster_id": cluster_label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
