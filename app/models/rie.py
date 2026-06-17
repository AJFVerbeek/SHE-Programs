"""SQLAlchemy-modellen voor de RI&E (Risico-Inventarisatie & -Evaluatie)."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.scoring import calculate_risk_score, classify_risk


class Assessment(Base):
    """Een RI&E voor een afdeling, locatie of activiteit."""

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    department: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    hazards: Mapped[list["Hazard"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
        order_by="Hazard.id",
    )


class Hazard(Base):
    """Een geinventariseerd gevaar met Fine & Kinney-beoordeling."""

    __tablename__ = "hazards"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE")
    )
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Fine & Kinney-factoren.
    probability: Mapped[float] = mapped_column(Float)  # Waarschijnlijkheid (W)
    exposure: Mapped[float] = mapped_column(Float)  # Blootstelling (B)
    effect: Mapped[float] = mapped_column(Float)  # Effect (E)

    control_measure: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Restrisico: herbeoordeling na het treffen van de beheersmaatregel.
    # Optioneel; alleen ingevuld wanneer een herbeoordeling is gedaan.
    residual_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    residual_exposure: Mapped[float | None] = mapped_column(Float, nullable=True)
    residual_effect: Mapped[float | None] = mapped_column(Float, nullable=True)

    assessment: Mapped["Assessment"] = relationship(back_populates="hazards")

    @property
    def risk_score(self) -> float:
        """Het berekende Fine & Kinney-risicogetal (W x B x E)."""
        return calculate_risk_score(self.probability, self.exposure, self.effect)

    @property
    def risk_label(self) -> str:
        """De tekstuele risicoklasse (bijv. 'Hoog')."""
        return classify_risk(self.risk_score).label

    @property
    def risk_action(self) -> str:
        """De geadviseerde actie horend bij de risicoklasse."""
        return classify_risk(self.risk_score).action

    @property
    def has_residual(self) -> bool:
        """Of er een volledige restrisico-herbeoordeling beschikbaar is."""
        return None not in (
            self.residual_probability,
            self.residual_exposure,
            self.residual_effect,
        )

    @property
    def residual_risk_score(self) -> float | None:
        """Het restrisicogetal na maatregel, of None als niet beoordeeld."""
        if not self.has_residual:
            return None
        return calculate_risk_score(
            self.residual_probability,
            self.residual_exposure,
            self.residual_effect,
        )

    @property
    def residual_risk_label(self) -> str | None:
        """De restrisicoklasse na maatregel, of None als niet beoordeeld."""
        score = self.residual_risk_score
        return classify_risk(score).label if score is not None else None
