"""Integratietests voor de RI&E-API.

De gedeelde `client`-fixture staat in conftest.py.
"""


def test_create_assessment_and_add_hazard(client):
    resp = client.post(
        "/api/assessments",
        json={"title": "RI&E Magazijn", "department": "Logistiek"},
    )
    assert resp.status_code == 201
    assessment_id = resp.json()["id"]

    resp = client.post(
        f"/api/assessments/{assessment_id}/hazards",
        json={
            "description": "Vallen van hoogte",
            "category": "Fysiek",
            "probability": 6,
            "exposure": 6,
            "effect": 15,
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["risk_score"] == 540
    assert body["risk_label"] == "Zeer hoog"


def test_invalid_factor_rejected(client):
    resp = client.post(
        "/api/assessments",
        json={"title": "Test", "department": "X"},
    )
    assessment_id = resp.json()["id"]

    resp = client.post(
        f"/api/assessments/{assessment_id}/hazards",
        json={
            "description": "Ongeldig",
            "probability": 7,  # niet toegestaan in de schaal
            "exposure": 6,
            "effect": 15,
        },
    )
    assert resp.status_code == 422


def test_get_unknown_assessment_returns_404(client):
    assert client.get("/api/assessments/9999").status_code == 404


def test_rename_assessment(client):
    resp = client.post(
        "/api/assessments",
        json={"title": "Oude titel", "department": "Logistiek"},
    )
    assessment_id = resp.json()["id"]

    resp = client.patch(
        f"/api/assessments/{assessment_id}",
        json={"title": "Nieuwe titel", "department": "Productie"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "Nieuwe titel"
    assert body["department"] == "Productie"

    # Wijziging is opgeslagen.
    resp = client.get(f"/api/assessments/{assessment_id}")
    assert resp.json()["title"] == "Nieuwe titel"


def test_rename_unknown_assessment_returns_404(client):
    resp = client.patch(
        "/api/assessments/9999",
        json={"title": "X", "department": "Y"},
    )
    assert resp.status_code == 404


def test_pdf_export(client):
    resp = client.post(
        "/api/assessments",
        json={"title": "RI&E Magazijn", "department": "Logistiek"},
    )
    assessment_id = resp.json()["id"]
    client.post(
        f"/api/assessments/{assessment_id}/hazards",
        json={
            "description": "Vallen van hoogte",
            "probability": 6,
            "exposure": 6,
            "effect": 15,
        },
    )

    resp = client.get(f"/assessments/{assessment_id}/pdf")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF")


def test_pdf_export_unknown_returns_404(client):
    assert client.get("/assessments/9999/pdf").status_code == 404


def _create_hazard(client, **overrides):
    """Hulpfunctie: maak een RI&E met een gevaar en geef (assessment_id, hazard)."""
    assessment_id = client.post(
        "/api/assessments", json={"title": "T", "department": "D"}
    ).json()["id"]
    payload = {
        "description": "Vallen van hoogte",
        "probability": 6,
        "exposure": 6,
        "effect": 15,
    }
    payload.update(overrides)
    hazard = client.post(
        f"/api/assessments/{assessment_id}/hazards", json=payload
    ).json()
    return assessment_id, hazard


def test_residual_risk_calculated(client):
    _, hazard = _create_hazard(
        client,
        residual_probability=3,
        residual_exposure=6,
        residual_effect=3,
    )
    assert hazard["residual_risk_score"] == 54
    assert hazard["residual_risk_label"] == "Mogelijk"


def test_residual_risk_optional(client):
    _, hazard = _create_hazard(client)
    assert hazard["residual_risk_score"] is None
    assert hazard["residual_risk_label"] is None


def test_residual_must_be_complete(client):
    assessment_id = client.post(
        "/api/assessments", json={"title": "T", "department": "D"}
    ).json()["id"]
    resp = client.post(
        f"/api/assessments/{assessment_id}/hazards",
        json={
            "description": "Onvolledig restrisico",
            "probability": 6,
            "exposure": 6,
            "effect": 15,
            "residual_probability": 3,  # B en E ontbreken
        },
    )
    assert resp.status_code == 422


def test_update_hazard(client):
    _, hazard = _create_hazard(client)
    resp = client.patch(
        f"/api/hazards/{hazard['id']}",
        json={
            "description": "Aangepast gevaar",
            "probability": 1,
            "exposure": 1,
            "effect": 3,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["description"] == "Aangepast gevaar"
    assert body["risk_score"] == 3


def test_delete_hazard(client):
    assessment_id, hazard = _create_hazard(client)
    assert client.delete(f"/api/hazards/{hazard['id']}").status_code == 204

    detail = client.get(f"/api/assessments/{assessment_id}").json()
    assert detail["hazards"] == []


def test_update_unknown_hazard_returns_404(client):
    resp = client.patch(
        "/api/hazards/9999",
        json={"description": "X", "probability": 1, "exposure": 1, "effect": 3},
    )
    assert resp.status_code == 404
