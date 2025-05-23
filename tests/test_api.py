import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from httpx import AsyncClient, ASGITransport
from api import app, API_KEY

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_analyze_ticket_no_auth():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/analyze-ticket", json={
            "subject": "URGENT: account hacked",
            "body": "Someone accessed my account and changed the email address.",
            "lang": "en"
        })
    assert r.status_code == 403

@pytest.mark.asyncio
async def test_analyze_ticket_invalid_token():
    transport = ASGITransport(app=app)
    headers = {"Authorization": "Bearer wrongtoken"}
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        r = await client.post("/analyze-ticket", json={
            "subject": "URGENT: account hacked",
            "body": "Someone accessed my account and changed the email address.",
            "lang": "en"
        })
    assert r.status_code == 403

@pytest.mark.asyncio
async def test_analyze_ticket_success():
    transport = ASGITransport(app=app)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "subject": "URGENT: account hacked",
        "body": "Someone accessed my account and changed the email address.",
        "lang": "en"
    }
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        r = await client.post("/analyze-ticket", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "urgency_score" in data and 0.0 <= data["urgency_score"] <= 1.0
    assert "cluster_id" in data and isinstance(data["cluster_id"], int)

@pytest.mark.asyncio
async def test_analyze_ticket_bad_request_with_auth():
    transport = ASGITransport(app=app)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        r = await client.post("/analyze-ticket", json={"subject": "Missing body"})
    assert r.status_code == 422
