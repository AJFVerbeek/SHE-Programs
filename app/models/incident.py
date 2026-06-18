"""SQLAlchemy-model voor de incidentregistratie."""

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.incidents import IncidentStatus, IncidentType, Severity


class Incident(Base):
    """Een geregistreerd incident (ongeval, bijna-ongeval, etc.)."""

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(200))
    occurred_on: Mapped[date] = mapped_column(Date)

    incident_type: Mapped[IncidentType] = mapped_column(
        Enum(IncidentType, native_enum=False, length=50)
    )
    severity: Mapped[Severity] = mapped_column(
        Enum(Severity, native_enum=False, length=50)
    )
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, native_enum=False, length=50),
        default=IncidentStatus.OPEN,
    )

    corrective_action: Mapped[str | None] = mapped_column(Text, nullable=True)

    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
