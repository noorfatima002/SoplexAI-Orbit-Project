from app.models import AuditLog
from app.services.domain import normalize_domain


def test_normalize_domain():
    assert normalize_domain("https://www.Acme.com/about") == "acme.com"
    assert normalize_domain("ACME.com") == "acme.com"
    assert normalize_domain("acme.com:8080/x") == "acme.com"


def test_api_key_is_required(client):
    assert client.get("/api/v1/companies", headers={"X-API-Key": "wrong"}).status_code == 401


def test_create_company_derives_domain_and_writes_audit_log(client, db_session):
    response = client.post("/api/v1/companies", json={"name": "Acme Digital", "website": "https://www.Acme.com/about"})
    assert response.status_code == 201
    assert response.json()["domain"] == "acme.com"
    assert db_session.query(AuditLog).filter_by(action="company.created").count() == 1


def test_duplicate_domain_returns_409(client):
    client.post("/api/v1/companies", json={"name": "Acme", "domain": "acme.com"})
    response = client.post("/api/v1/companies", json={"name": "Acme Again", "website": "https://ACME.com"})
    assert response.status_code == 409


def test_validation_errors_return_422(client):
    assert client.post("/api/v1/companies", json={"name": "", "domain": "acme.com"}).status_code == 422
    assert client.post("/api/v1/companies", json={"name": "No Domain"}).status_code == 422


def test_list_and_get_company(client):
    created = client.post("/api/v1/companies", json={"name": "Acme", "domain": "acme.com"}).json()
    assert client.get("/api/v1/companies").json()[0]["id"] == created["id"]
    assert client.get(f"/api/v1/companies/{created['id']}").status_code == 200
    assert client.get("/api/v1/companies/9999").status_code == 404
