"""Webinterface (server-rendered) voor de incidentregistratie."""

from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.incidents import IncidentStatus, IncidentType, Severity
from app.schemas import IncidentCreate

router = APIRouter(prefix="/incidents", tags=["web-incidenten"])

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))

# Keuzelijsten die elke template-context nodig heeft.
_CHOICES = {
    "types": list(IncidentType),
    "severities": list(Severity),
    "statuses": list(IncidentStatus),
}


@router.get("", response_class=HTMLResponse)
def incidents_index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Overzichtspagina met alle incidenten."""
    incidents = crud.incident.list_incidents(db)
    return templates.TemplateResponse(
        request,
        "incidents_index.html",
        {"incidents": incidents, "today": date.today().isoformat(), **_CHOICES},
    )


@router.post("")
def create_incident_form(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    occurred_on: date = Form(...),
    incident_type: IncidentType = Form(...),
    severity: Severity = Form(...),
    status_value: IncidentStatus = Form(IncidentStatus.OPEN, alias="status"),
    corrective_action: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Registreer een incident vanuit het formulier."""
    incident = crud.incident.create_incident(
        db,
        IncidentCreate(
            title=title,
            description=description,
            location=location,
            occurred_on=occurred_on,
            incident_type=incident_type,
            severity=severity,
            status=status_value,
            corrective_action=corrective_action or None,
        ),
    )
    return RedirectResponse(
        f"/incidents/{incident.id}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/{incident_id}", response_class=HTMLResponse)
def incident_detail(
    incident_id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    """Detail-/bewerkpagina van een incident."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    return templates.TemplateResponse(
        request,
        "incident_detail.html",
        {"incident": incident, **_CHOICES},
    )


@router.post("/{incident_id}/edit")
def edit_incident_form(
    incident_id: int,
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    occurred_on: date = Form(...),
    incident_type: IncidentType = Form(...),
    severity: Severity = Form(...),
    status_value: IncidentStatus = Form(..., alias="status"),
    corrective_action: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Sla wijzigingen aan een incident op."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    crud.incident.update_incident(
        db,
        incident,
        IncidentCreate(
            title=title,
            description=description,
            location=location,
            occurred_on=occurred_on,
            incident_type=incident_type,
            severity=severity,
            status=status_value,
            corrective_action=corrective_action or None,
        ),
    )
    return RedirectResponse(
        f"/incidents/{incident_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/{incident_id}/delete")
def delete_incident_form(
    incident_id: int, db: Session = Depends(get_db)
) -> RedirectResponse:
    """Verwijder een incident."""
    incident = crud.incident.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incident niet gevonden")
    crud.incident.delete_incident(db, incident)
    return RedirectResponse("/incidents", status_code=status.HTTP_303_SEE_OTHER)
