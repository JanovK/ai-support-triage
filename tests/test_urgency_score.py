import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from urgency_score import hybrid_urgency_score

def test_urgent_ticket_high_score():
    ticket = {
        "ticket_id": "T001",
        "subject": "URGENT: Security breach",
        "body": "My account was hacked. Need help now!"
    }
    scored = hybrid_urgency_score(ticket)
    assert scored["urgency_score"] > 0.8
    assert scored["urgency_reason"]["sentiment"] in ["NEGATIVE", "POSITIVE"]

def test_low_priority_ticket():
    ticket = {
        "ticket_id": "T002",
        "subject": "Question about features",
        "body": "Can you tell me more about the pricing options?"
    }
    scored = hybrid_urgency_score(ticket)
    assert scored["urgency_score"] < 0.5
