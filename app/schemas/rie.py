"""Pydantic-schema's voor de RI&E-module."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.scoring import EFFECT_VALUES, EXPOSURE_VALUES, PROBABILITY_VALUES


def _in_scale(value: float | None, allowed: tuple[float, ...], name: str) -> float | None:
    """Valideer een (optionele) factor tegen de toegestane Fine & Kinney-schaal."""
    if value is not None and value not in allowed:
        raise ValueError(f"{name} moet een van {allowed} zijn")
    return value


class HazardCreate(BaseModel):
    """Invoer voor het aanmaken of wijzigen van een gevaar."""

    description: str = Field(min_length=1, max_length=2000)
    category: str | None = Field(default=None, max_length=100)
    probability: float = Field(description=f"Waarschijnlijkheid, een van {PROBABILITY_VALUES}")
    exposure: float = Field(description=f"Blootstelling, een van {EXPOSURE_VALUES}")
    effect: float = Field(description=f"Effect, een van {EFFECT_VALUES}")
    control_measure: str | None = Field(default=None, max_length=2000)

    # Restrisico na maatregel (optioneel, maar alles-of-niets).
    residual_probability: float | None = Field(default=None)
    residual_exposure: float | None = Field(default=None)
    residual_effect: float | None = Field(default=None)

    @field_validator("probability")
    @classmethod
    def _check_probability(cls, v: float) -> float:
        return _in_scale(v, PROBABILITY_VALUES, "Waarschijnlijkheid")

    @field_validator("exposure")
    @classmethod
    def _check_exposure(cls, v: float) -> float:
        return _in_scale(v, EXPOSURE_VALUES, "Blootstelling")

    @field_validator("effect")
    @classmethod
    def _check_effect(cls, v: float) -> float:
        return _in_scale(v, EFFECT_VALUES, "Effect")

    @field_validator("residual_probability")
    @classmethod
    def _check_res_probability(cls, v: float | None) -> float | None:
        return _in_scale(v, PROBABILITY_VALUES, "Rest-waarschijnlijkheid")

    @field_validator("residual_exposure")
    @classmethod
    def _check_res_exposure(cls, v: float | None) -> float | None:
        return _in_scale(v, EXPOSURE_VALUES, "Rest-blootstelling")

    @field_validator("residual_effect")
    @classmethod
    def _check_res_effect(cls, v: float | None) -> float | None:
        return _in_scale(v, EFFECT_VALUES, "Rest-effect")

    @model_validator(mode="after")
    def _check_residual_complete(self) -> "HazardCreate":
        residual = (
            self.residual_probability,
            self.residual_exposure,
            self.residual_effect,
        )
        if any(v is not None for v in residual) and any(v is None for v in residual):
            raise ValueError(
                "Restrisico moet volledig zijn (W, B en E) of helemaal leeg blijven"
            )
        return self


class HazardRead(BaseModel):
    """Uitvoer van een gevaar, inclusief berekende risicowaarden."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    category: str | None
    probability: float
    exposure: float
    effect: float
    control_measure: str | None
    risk_score: float
    risk_label: str
    risk_action: str
    residual_probability: float | None
    residual_exposure: float | None
    residual_effect: float | None
    residual_risk_score: float | None
    residual_risk_label: str | None


class AssessmentCreate(BaseModel):
    """Invoer voor het aanmaken van een RI&E."""

    title: str = Field(min_length=1, max_length=200)
    department: str = Field(min_length=1, max_length=200)


class AssessmentUpdate(BaseModel):
    """Invoer voor het wijzigen van een RI&E (titel/afdeling)."""

    title: str = Field(min_length=1, max_length=200)
    department: str = Field(min_length=1, max_length=200)


class AssessmentRead(BaseModel):
    """Uitvoer van een RI&E zonder gevaren."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    department: str
    created_at: datetime


class AssessmentDetail(AssessmentRead):
    """Uitvoer van een RI&E inclusief de bijbehorende gevaren."""

    hazards: list[HazardRead] = []
