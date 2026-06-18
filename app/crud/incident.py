"""CRUD-operaties voor de incidentregistratie."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Incident
from app.schemas import IncidentCreate


def list_incidents(db: Session) -> list[Incident]:
    """Geef alle incidenten terug, op datum aflopend (nieuwste eerst)."""
    return list(
        db.scalars(
            select(Incident).order_by(
                Incident.occurred_on.desc(), Incident.id.desc()
            )
        )
    )


def get_incident(db: Session, incident_id: int) -> Incident | None:
    """Haal een enkel incident op, of None als het niet bestaat."""
    return db.get(Incident, incident_id)


def create_incident(db: Session, data: IncidentCreate) -> Incident:
    """Registreer een nieuw incident."""
    incident = Incident(**data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def update_incident(db: Session, incident: Incident, data: IncidentCreate) -> Incident:
    """Wijzig een bestaand incident."""
    for field, value in data.model_dump().items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return incident


def delete_incident(db: Session, incident: Incident) -> None:
    """Verwijder een incident."""
    db.delete(incident)
    db.commit()
