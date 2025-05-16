import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from httpx import AsyncClient, ASGITransport
from api import app, API_KEY

@pytest.mark.asyncio
async def test_analyze_ticket_cluster_id():
    transport = ASGITransport(app=app)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"subject": "Login problem", "body": "Cannot log into my account.", "lang":"en"}
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        r = await client.post("/analyze-ticket", json=payload)
    data = r.json()
    assert isinstance(data["cluster_id"], int)
