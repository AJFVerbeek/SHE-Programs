"""Tests voor de rapportgenerator."""

from rie_toetsing import criteria
from rie_toetsing.rapport import render


def _voorbeeld_data():
    return {
        "organisatieprofiel": {
            "organisatienaam": "Voorbeeld B.V.",
            "branche_sbi": "43.99",
            "aantal_medewerkers": "120",
            "datum_rie": "2025-01-01",
            "gebruikt_instrument": "Branche-RI&E Bouw",
            "toetsingsdatum": "2026-06-20",
        },
        "toetsingen": [
            {"id": c.id, "oordeel": "Ja", "bevinding": f"Bevinding {c.id}",
             "advies": f"Advies {c.id}"}
            for c in criteria.ALLE_CRITERIA
        ],
        "oordeel_volledigheid": "Voldoende.",
        "oordeel_actualiteit": "Actueel.",
        "oordeel_betrouwbaarheid": "Betrouwbaar.",
        "advies_plan_van_aanpak": "PvA is SMART.",
        "verdiepende_onderzoeken": ["PSA-onderzoek", "Geluidmeting"],
        "scope_ah": "AH-toelichting.",
        "scope_hvk": "HVK-toelichting.",
        "scope_ao": "A&O-toelichting.",
        "samenvatting": "Eindoordeel voldoende.",
    }


def test_render_bevat_kernonderdelen():
    md = render(_voorbeeld_data())
    assert "# Toets- en adviesrapport" in md
    assert "Voorbeeld B.V." in md
    assert "## 1. Toetsen van de RI&E" in md
    assert "## 2. Toetsen van het Plan van Aanpak" in md
    assert "Samenvatting per scope" in md
    assert "André" in md  # AKD-ondertekening


def test_render_bevat_alle_criteria():
    md = render(_voorbeeld_data())
    for crit in criteria.ALLE_CRITERIA:
        assert crit.id in md
    # RAG-codering voor 'Ja' moet zichtbaar zijn.
    assert "🟢" in md


def test_render_verdiepende_onderzoeken():
    md = render(_voorbeeld_data())
    assert "- PSA-onderzoek" in md
    assert "- Geluidmeting" in md


def test_render_leeg_sjabloon():
    md = render({})
    assert "[in te vullen]" in md
    # Ook zonder data moeten alle toetsregels in het sjabloon staan.
    for crit in criteria.ALLE_CRITERIA:
        assert crit.id in md


def test_geen_fine_kinney_terminologie():
    md = render(_voorbeeld_data()).lower()
    assert "fine-kinney" not in md
    assert "fine kinney" not in md
