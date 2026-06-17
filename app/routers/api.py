"""JSON-API voor de RI&E-module."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import (
    AssessmentCreate,
    AssessmentDetail,
    AssessmentRead,
    AssessmentUpdate,
    HazardCreate,
    HazardRead,
)

router = APIRouter(prefix="/api", tags=["RI&E"])


@router.get("/assessments", response_model=list[AssessmentRead])
def list_assessments(db: Session = Depends(get_db)) -> list:
    """Lijst van alle RI&E's."""
    return crud.rie.list_assessments(db)


@router.post(
    "/assessments",
    response_model=AssessmentDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_assessment(
    data: AssessmentCreate, db: Session = Depends(get_db)
) -> object:
    """Maak een nieuwe RI&E aan."""
    return crud.rie.create_assessment(db, data)


@router.get("/assessments/{assessment_id}", response_model=AssessmentDetail)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)) -> object:
    """Haal een RI&E op inclusief gevaren."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    return assessment


@router.patch("/assessments/{assessment_id}", response_model=AssessmentDetail)
def update_assessment(
    assessment_id: int, data: AssessmentUpdate, db: Session = Depends(get_db)
) -> object:
    """Wijzig de titel/afdeling van een RI&E."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    return crud.rie.update_assessment(db, assessment, data)


@router.delete(
    "/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_assessment(assessment_id: int, db: Session = Depends(get_db)) -> None:
    """Verwijder een RI&E."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    crud.rie.delete_assessment(db, assessment)


@router.post(
    "/assessments/{assessment_id}/hazards",
    response_model=HazardRead,
    status_code=status.HTTP_201_CREATED,
)
def add_hazard(
    assessment_id: int, data: HazardCreate, db: Session = Depends(get_db)
) -> object:
    """Voeg een gevaar toe aan een RI&E."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    try:
        return crud.rie.add_hazard(db, assessment, data)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
