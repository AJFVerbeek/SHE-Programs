"""Integratietests voor de incidentregistratie."""


def _payload(**overrides):
    data = {
        "title": "Uitglijden in magazijn",
        "description": "Medewerker uitgegleden over natte vloer.",
        "location": "Magazijn",
        "occurred_on": "2026-06-01",
        "incident_type": "Bijna-ongeval",
        "severity": "Geen letsel",
    }
    data.update(overrides)
    return data


def test_create_and_get_incident(client):
    resp = client.post("/api/incidents", json=_payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "Open"  # standaardstatus
    incident_id = body["id"]

    resp = client.get(f"/api/incidents/{incident_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Uitglijden in magazijn"


def test_invalid_enum_rejected(client):
    resp = client.post("/api/incidents", json=_payload(severity="Heel erg"))
    assert resp.status_code == 422


def test_update_incident_status(client):
    incident_id = client.post("/api/incidents", json=_payload()).json()["id"]
    resp = client.patch(
        f"/api/incidents/{incident_id}",
        json=_payload(status="Afgehandeld", corrective_action="Vloer gemarkeerd"),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "Afgehandeld"
    assert body["corrective_action"] == "Vloer gemarkeerd"


def test_delete_incident(client):
    incident_id = client.post("/api/incidents", json=_payload()).json()["id"]
    assert client.delete(f"/api/incidents/{incident_id}").status_code == 204
    assert client.get(f"/api/incidents/{incident_id}").status_code == 404


def test_list_incidents(client):
    client.post("/api/incidents", json=_payload(title="A"))
    client.post("/api/incidents", json=_payload(title="B"))
    resp = client.get("/api/incidents")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_unknown_incident_returns_404(client):
    assert client.patch("/api/incidents/9999", json=_payload()).status_code == 404


def test_web_incidents_pages(client):
    # Overzichtspagina laadt.
    assert client.get("/incidents").status_code == 200
    # Aanmaken via formulier en doorverwijzing naar detail.
    resp = client.post(
        "/incidents",
        data={
            "title": "Test",
            "description": "Toelichting",
            "location": "Kantoor",
            "occurred_on": "2026-06-10",
            "incident_type": "Onveilige situatie",
            "severity": "Geen letsel",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Test" in resp.text
