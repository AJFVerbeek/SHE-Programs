"""PDF-export van een RI&E met ReportLab."""

from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.models import Assessment

# Kleur per risicoklasse (overeenkomstig de badges in de webinterface).
_RISK_COLORS: dict[str, colors.Color] = {
    "Gering": colors.HexColor("#2f855a"),
    "Mogelijk": colors.HexColor("#b7791f"),
    "Substantieel": colors.HexColor("#c05621"),
    "Hoog": colors.HexColor("#c53030"),
    "Zeer hoog": colors.HexColor("#7b1d1d"),
}

_HEADER = ["Gevaar", "Categorie", "W", "B", "E", "Risico", "Klasse", "Beheersmaatregel"]


def build_assessment_pdf(assessment: Assessment) -> bytes:
    """Genereer een PDF van een RI&E en geef de bytes terug."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f"RI&E - {assessment.title}",
    )

    styles = getSampleStyleSheet()
    cell = ParagraphStyle("cell", parent=styles["BodyText"], fontSize=8, leading=10)
    cell_center = ParagraphStyle("cellc", parent=cell, alignment=TA_CENTER)
    head_cell = ParagraphStyle(
        "headcell", parent=cell, textColor=colors.white, fontName="Helvetica-Bold"
    )

    elements: list = []
    elements.append(Paragraph(assessment.title, styles["Title"]))
    elements.append(
        Paragraph(f"Afdeling/locatie: {assessment.department}", styles["Normal"])
    )
    elements.append(
        Paragraph(
            f"Geexporteerd op: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 8 * mm))

    # Tabelinhoud opbouwen.
    data: list[list] = [[Paragraph(h, head_cell) for h in _HEADER]]
    risk_row_styles: list = []

    if assessment.hazards:
        for row_index, h in enumerate(assessment.hazards, start=1):
            data.append(
                [
                    Paragraph(h.description, cell),
                    Paragraph(h.category or "-", cell),
                    Paragraph(str(h.probability), cell_center),
                    Paragraph(str(h.exposure), cell_center),
                    Paragraph(str(h.effect), cell_center),
                    Paragraph(f"<b>{h.risk_score}</b>", cell_center),
                    Paragraph(h.risk_label, cell_center),
                    Paragraph(h.control_measure or "-", cell),
                ]
            )
            color = _RISK_COLORS.get(h.risk_label, colors.grey)
            risk_row_styles.append(("BACKGROUND", (6, row_index), (6, row_index), color))
            risk_row_styles.append(("TEXTCOLOR", (6, row_index), (6, row_index), colors.white))
    else:
        data.append([Paragraph("Nog geen gevaren geinventariseerd.", cell)] + [""] * 7)

    col_widths = [60 * mm, 28 * mm, 12 * mm, 12 * mm, 12 * mm, 18 * mm, 26 * mm, 80 * mm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d6f42")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fa")]),
                *risk_row_styles,
            ]
        )
    )
    elements.append(table)

    elements.append(Spacer(1, 6 * mm))
    elements.append(
        Paragraph(
            "Risico = Waarschijnlijkheid (W) x Blootstelling (B) x Effect (E) "
            "&mdash; Fine &amp; Kinney-methode",
            ParagraphStyle("foot", parent=styles["Normal"], fontSize=8,
                           textColor=colors.HexColor("#6b7280")),
        )
    )

    doc.build(elements)
    return buffer.getvalue()
