def test_run_agent_is_idempotent(client):
    body = {"agent": "lead_generation", "params": {"limit": 10}, "idempotency_key": "run-1"}
    first = client.post("/api/v1/agents/run", json=body)
    second = client.post("/api/v1/agents/run", json=body)
    assert first.status_code == 202
    assert first.json()["status"] == "queued"
    assert second.json()["id"] == first.json()["id"]


def test_agents_not_in_v1_return_501(client):
    assert client.post("/api/v1/agents/run", json={"agent": "outreach"}).status_code == 501


def test_unknown_agent_returns_422(client):
    assert client.post("/api/v1/agents/run", json={"agent": "nope"}).status_code == 422


def test_get_job(client):
    job = client.post("/api/v1/agents/run", json={"agent": "lead_generation"}).json()
    assert client.get(f"/api/v1/agents/jobs/{job['id']}").status_code == 200
    assert client.get("/api/v1/agents/jobs/9999").status_code == 404
