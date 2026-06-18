"""JSON-API voor de incidentregistratie."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import IncidentCreate, IncidentRead

router = APIRouter(prefix="/api/incidents", tags=["Incidenten"])


@router.get("", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)) -> list:
    """Lijst van alle incidenten."""
    return crud.incident.list_incidents(db)


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(data: IncidentCreate, db: Session = Depends(get_db)) -> object:
    """Registreer een nieuw incident."""
    return crud.incident.create_incident(db, data)


@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)) -> object:
    """Haal een incident op."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    return incident


@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident(
    incident_id: int, data: IncidentCreate, db: Session = Depends(get_db)
) -> object:
    """Wijzig een incident."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    return crud.incident.update_incident(db, incident, data)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)) -> None:
    """Verwijder een incident."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    crud.incident.delete_incident(db, incident)
