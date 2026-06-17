"""Pydantic-schema's voor de RI&E-module."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.scoring import EFFECT_VALUES, EXPOSURE_VALUES, PROBABILITY_VALUES


class HazardCreate(BaseModel):
    """Invoer voor het aanmaken van een gevaar."""

    description: str = Field(min_length=1, max_length=2000)
    category: str | None = Field(default=None, max_length=100)
    probability: float = Field(description=f"Waarschijnlijkheid, een van {PROBABILITY_VALUES}")
    exposure: float = Field(description=f"Blootstelling, een van {EXPOSURE_VALUES}")
    effect: float = Field(description=f"Effect, een van {EFFECT_VALUES}")
    control_measure: str | None = Field(default=None, max_length=2000)

    @field_validator("probability")
    @classmethod
    def _check_probability(cls, v: float) -> float:
        if v not in PROBABILITY_VALUES:
            raise ValueError(f"Waarschijnlijkheid moet een van {PROBABILITY_VALUES} zijn")
        return v

    @field_validator("exposure")
    @classmethod
    def _check_exposure(cls, v: float) -> float:
        if v not in EXPOSURE_VALUES:
            raise ValueError(f"Blootstelling moet een van {EXPOSURE_VALUES} zijn")
        return v

    @field_validator("effect")
    @classmethod
    def _check_effect(cls, v: float) -> float:
        if v not in EFFECT_VALUES:
            raise ValueError(f"Effect moet een van {EFFECT_VALUES} zijn")
        return v


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
