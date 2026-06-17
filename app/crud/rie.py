"""CRUD-operaties voor RI&E's en gevaren."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Assessment, Hazard
from app.schemas import AssessmentCreate, AssessmentUpdate, HazardCreate


def list_assessments(db: Session) -> list[Assessment]:
    """Geef alle RI&E's terug, nieuwste eerst."""
    return list(db.scalars(select(Assessment).order_by(Assessment.id.desc())))


def get_assessment(db: Session, assessment_id: int) -> Assessment | None:
    """Haal een enkele RI&E op, of None als die niet bestaat."""
    return db.get(Assessment, assessment_id)


def create_assessment(db: Session, data: AssessmentCreate) -> Assessment:
    """Maak een nieuwe RI&E aan."""
    assessment = Assessment(title=data.title, department=data.department)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


def update_assessment(
    db: Session, assessment: Assessment, data: AssessmentUpdate
) -> Assessment:
    """Wijzig de titel en afdeling van een RI&E."""
    assessment.title = data.title
    assessment.department = data.department
    db.commit()
    db.refresh(assessment)
    return assessment


def delete_assessment(db: Session, assessment: Assessment) -> None:
    """Verwijder een RI&E inclusief de bijbehorende gevaren."""
    db.delete(assessment)
    db.commit()


def add_hazard(db: Session, assessment: Assessment, data: HazardCreate) -> Hazard:
    """Voeg een gevaar toe aan een RI&E.

    De Fine & Kinney-factoren worden door het Pydantic-schema en het
    scoring-model gevalideerd; ongeldige waarden leiden tot een ValueError.
    """
    hazard = Hazard(
        assessment_id=assessment.id,
        description=data.description,
        category=data.category,
        probability=data.probability,
        exposure=data.exposure,
        effect=data.effect,
        control_measure=data.control_measure,
    )
    db.add(hazard)
    db.commit()
    db.refresh(hazard)
    return hazard


def delete_hazard(db: Session, hazard: Hazard) -> None:
    """Verwijder een gevaar."""
    db.delete(hazard)
    db.commit()
