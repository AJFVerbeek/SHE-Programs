"""Webinterface (server-rendered) voor de RI&E-module."""

from pathlib import Path

import re

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.pdf import build_assessment_pdf
from app.schemas import AssessmentCreate, HazardCreate
from app.scoring import EFFECT_VALUES, EXPOSURE_VALUES, PROBABILITY_VALUES


def _safe_filename(name: str) -> str:
    """Maak een veilige bestandsnaam van een vrije tekst."""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return slug or "rie"

router = APIRouter(tags=["web"])

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Overzichtspagina met alle RI&E's."""
    assessments = crud.rie.list_assessments(db)
    return templates.TemplateResponse(
        request, "index.html", {"assessments": assessments}
    )


@router.post("/assessments")
def create_assessment_form(
    title: str = Form(...),
    department: str = Form(...),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Maak een RI&E aan vanuit het formulier."""
    assessment = crud.rie.create_assessment(
        db, AssessmentCreate(title=title, department=department)
    )
    return RedirectResponse(
        f"/assessments/{assessment.id}", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/assessments/{assessment_id}", response_class=HTMLResponse)
def assessment_detail(
    assessment_id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    """Detailpagina van een RI&E met gevaren en risicobeoordeling."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    return templates.TemplateResponse(
        request,
        "detail.html",
        {
            "assessment": assessment,
            "probability_values": PROBABILITY_VALUES,
            "exposure_values": EXPOSURE_VALUES,
            "effect_values": EFFECT_VALUES,
        },
    )


@router.get("/assessments/{assessment_id}/pdf")
def assessment_pdf(
    assessment_id: int, db: Session = Depends(get_db)
) -> Response:
    """Exporteer een RI&E als PDF-bestand."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    pdf_bytes = build_assessment_pdf(assessment)
    filename = f"RIE_{_safe_filename(assessment.title)}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/assessments/{assessment_id}/hazards")
def add_hazard_form(
    assessment_id: int,
    description: str = Form(...),
    category: str = Form(""),
    probability: float = Form(...),
    exposure: float = Form(...),
    effect: float = Form(...),
    control_measure: str = Form(""),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """Voeg een gevaar toe vanuit het formulier."""
    assessment = crud.rie.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "RI&E niet gevonden")
    crud.rie.add_hazard(
        db,
        assessment,
        HazardCreate(
            description=description,
            category=category or None,
            probability=probability,
            exposure=exposure,
            effect=effect,
            control_measure=control_measure or None,
        ),
    )
    return RedirectResponse(
        f"/assessments/{assessment_id}", status_code=status.HTTP_303_SEE_OTHER
    )
