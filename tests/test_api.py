import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from httpx import AsyncClient, ASGITransport
from api import app

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_analyze_ticket_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/analyze-ticket", json={
            "subject": "URGENT: account hacked",
            "body": "Someone accessed my account and changed the email address.",
            "lang": "en"
        })
    assert r.status_code == 200
    data = r.json()
    assert "urgency_score" in data and 0.0 <= data["urgency_score"] <= 1.0
    assert "cluster_id" in data and isinstance(data["cluster_id"], int)

@pytest.mark.asyncio
async def test_analyze_ticket_bad_request():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/analyze-ticket", json={"subject": "Missing body"})
    assert r.status_code == 422

