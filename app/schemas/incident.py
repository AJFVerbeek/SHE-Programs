"""Pydantic-schema's voor de incidentregistratie."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.incidents import IncidentStatus, IncidentType, Severity


class IncidentCreate(BaseModel):
    """Invoer voor het aanmaken of wijzigen van een incident."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    location: str = Field(min_length=1, max_length=200)
    occurred_on: date
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus = IncidentStatus.OPEN
    corrective_action: str | None = None


class IncidentRead(BaseModel):
    """Uitvoer van een incident."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    location: str
    occurred_on: date
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus
    corrective_action: str | None
    reported_at: datetime
