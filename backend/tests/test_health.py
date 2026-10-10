def test_root_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_v1_health_needs_no_key(client):
    response = client.get("/api/v1/health", headers={"X-API-Key": ""})
    assert response.status_code == 200


def test_database_health(client):
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"
