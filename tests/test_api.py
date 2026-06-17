"""Integratietests voor de RI&E-API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    """TestClient met een geisoleerde in-memory database."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


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
