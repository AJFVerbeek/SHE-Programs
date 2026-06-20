"""Opbouw van het Toets- en adviesrapport (Markdown) volgens het AMM-sjabloon v2.2."""

from __future__ import annotations

from datetime import date
from typing import Any

from .criteria import (
    ACTUALITEIT,
    ACTUELE_INZICHTEN,
    BETROUWBAARHEID,
    PLAN_VAN_AANPAK,
    RAG_KLEUR,
    VOLLEDIGHEID,
    Criterium,
)
from .prompt import AKD_GEGEVENS

_GEEN = "[in te vullen]"


def _oordeel_index(toetsingen: list[dict]) -> dict[str, dict]:
    """Maak een opzoektabel van criterium-id naar het toetsresultaat."""
    return {t.get("id", ""): t for t in toetsingen}


def _tabel(criteria: tuple[Criterium, ...], index: dict[str, dict]) -> list[str]:
    """Render één toetstabel met de kolommen uit het sjabloon."""
    regels = [
        "| # | Omschrijving criteria | Oordeel | Bevindingen | Advies |",
        "|---|---|---|---|---|",
    ]
    for crit in criteria:
        resultaat = index.get(crit.id, {})
        oordeel = resultaat.get("oordeel", "")
        rag = RAG_KLEUR.get(oordeel, "")
        oordeel_cel = f"{rag} {oordeel}".strip() or _GEEN
        bevinding = _cel(resultaat.get("bevinding"))
        advies = _cel(resultaat.get("advies"))
        omschrijving = crit.omschrijving.replace("|", "\\|")
        regels.append(
            f"| {crit.id} | {omschrijving} | {oordeel_cel} | {bevinding} | {advies} |"
        )
    return regels


def _cel(waarde: Any) -> str:
    """Maak tekst veilig voor een Markdown-tabelcel."""
    if not waarde:
        return _GEEN
    return str(waarde).replace("\n", " ").replace("|", "\\|").strip()


def _profielregel(label: str, waarde: Any) -> str:
    return f"| {label} | {waarde or _GEEN} |"


def render(data: dict[str, Any], *, toetsingsdatum: str | None = None) -> str:
    """Bouw het volledige Toets- en adviesrapport als Markdown-tekst.

    Args:
        data: Het toetsresultaat volgens ``prompt.UITVOER_SCHEMA``. Voor een leeg
            sjabloon (dry run) mag een leeg dict worden meegegeven.
        toetsingsdatum: Optionele toetsingsdatum; standaard vandaag.
    """
    profiel = data.get("organisatieprofiel", {})
    index = _oordeel_index(data.get("toetsingen", []))
    org = profiel.get("organisatienaam") or _GEEN
    datum = toetsingsdatum or profiel.get("toetsingsdatum") or date.today().isoformat()

    d: list[str] = []

    # ONDERDEEL A — Voorpagina
    d += [
        "# Toets- en adviesrapport Risico-Inventarisatie & -Evaluatie (RI&E)",
        "",
        f"**Organisatie:** {org}  ",
        f"**Datum toetsrapport:** {datum}  ",
        f"**Toetser:** {AKD_GEGEVENS['akd']} — {AKD_GEGEVENS['registratienummer']}  ",
        f"**Adviesbureau:** {AKD_GEGEVENS['organisatie']} · "
        f"{AKD_GEGEVENS['email']} · {AKD_GEGEVENS['telefoon']}",
        "",
        "---",
        "",
    ]

    # ONDERDEEL B — Samenvatting
    d += [
        "## Samenvatting",
        "",
        "Op grond van artikel 5 en 14 van de Arbowet en de toetsingscriteria in "
        "Staatscourant 2024 nr. 39674 is de RI&E getoetst op volledigheid, "
        "actualiteit, actuele inzichten en betrouwbaarheid.",
        "",
        f"**Oordeel volledigheid:** {data.get('oordeel_volledigheid') or _GEEN}",
        "",
        f"**Oordeel actualiteit:** {data.get('oordeel_actualiteit') or _GEEN}",
        "",
        f"**Oordeel betrouwbaarheid:** {data.get('oordeel_betrouwbaarheid') or _GEEN}",
        "",
        f"**Advies Plan van Aanpak:** {data.get('advies_plan_van_aanpak') or _GEEN}",
        "",
        "**Nog uit te voeren verdiepende onderzoeken:**",
        "",
    ]
    onderzoeken = data.get("verdiepende_onderzoeken") or []
    d += [f"- {o}" for o in onderzoeken] or [f"- {_GEEN}"]
    d += ["", "---", ""]

    # ONDERDEEL C — Basisgegevens
    d += [
        "## Basisgegevens",
        "",
        "| Gegeven | Waarde |",
        "|---|---|",
        _profielregel("Organisatienaam", profiel.get("organisatienaam")),
        _profielregel("Branche / SBI-code", profiel.get("branche_sbi")),
        _profielregel("Aantal medewerkers", profiel.get("aantal_medewerkers")),
        _profielregel("Datum RI&E", profiel.get("datum_rie")),
        _profielregel("Gebruikt RI&E-instrument", profiel.get("gebruikt_instrument")),
        _profielregel("Toetsingsdatum", datum),
        _profielregel("Toetser", AKD_GEGEVENS["akd"]),
        _profielregel("Registratienummer", AKD_GEGEVENS["registratienummer"]),
        "",
        "---",
        "",
    ]

    # ONDERDEEL D — Inleiding
    d += [
        "## Inleiding",
        "",
        "Op grond van artikel 5 van de Arbeidsomstandighedenwet is iedere werkgever "
        "verplicht een RI&E met een Plan van Aanpak op te stellen. Conform artikel 14 "
        "Arbowet en de toetsingscriteria in Staatscourant 2024 nr. 39674 dient de RI&E "
        "te worden getoetst door een gecertificeerde arbokerndeskundige op volledigheid, "
        "actualiteit, actuele inzichten en betrouwbaarheid.",
        "",
        "---",
        "",
    ]

    # ONDERDEEL E — Hoofdstuk 1: Toetsen van de RI&E
    d += ["## 1. Toetsen van de RI&E", ""]
    d += ["### Tabel 1.1 — Toetsen op volledigheid", ""]
    d += _tabel(VOLLEDIGHEID, index)
    d += ["", "### Tabel 1.2 — Toetsen op actualiteit", ""]
    d += _tabel(ACTUALITEIT, index)
    d += ["", "### Tabel 1.3 — Toetsen op actuele inzichten", ""]
    d += _tabel(ACTUELE_INZICHTEN, index)
    d += ["", "### Tabel 1.4 — Toetsen op betrouwbaarheid", ""]
    d += _tabel(BETROUWBAARHEID, index)
    d += ["", "---", ""]

    # ONDERDEEL F — Samenvatting per scope
    d += [
        "## Samenvatting per scope",
        "",
        "| Scope | Toelichting |",
        "|---|---|",
        f"| AH — Arbeidshygiëne | {_cel(data.get('scope_ah'))} |",
        f"| HVK — Hogere Veiligheidskunde | {_cel(data.get('scope_hvk'))} |",
        f"| A&O — Arbeids- en Organisatiedeskundige | {_cel(data.get('scope_ao'))} |",
        "",
        "---",
        "",
    ]

    # ONDERDEEL G — Hoofdstuk 2: Toetsen van het Plan van Aanpak
    d += ["## 2. Toetsen van het Plan van Aanpak", ""]
    d += _tabel(PLAN_VAN_AANPAK, index)
    d += ["", "---", ""]

    # ONDERDEEL H — Afronding
    d += [
        "## 3. Afronding van de toetsing",
        "",
        "De rapportage dient ter beschikking te worden gesteld aan de ondernemingsraad "
        "(OR) of personeelsvertegenwoordiging (PVT). De werkgever is conform artikel 14 "
        "lid 3 van de Arbowet verplicht een afschrift te zenden aan de belanghebbende "
        "werknemers.",
        "",
        "**Toetsing uitgevoerd door:**  ",
        f"{AKD_GEGEVENS['akd']}  ",
        "Arbeids- en Organisatiedeskundige (A&O) · Hogere Veiligheidskundige (HVK) · "
        "Arbeidshygiënist (AH)  ",
        f"{AKD_GEGEVENS['registratienummer']}  ",
        f"{AKD_GEGEVENS['organisatie']}  ",
        f"Datum: {datum}",
        "",
    ]
    if data.get("samenvatting"):
        d += ["> " + data["samenvatting"], ""]

    # ONDERDEEL I/J — Bijlagen + beperkingen
    d += [
        "---",
        "",
        "## Bijlagen",
        "",
        "- **Bijlage 1 — Verdiepende onderzoeken:** zie de opsomming in de samenvatting.",
        "- **Bijlage 2 — RI&E en Plan van Aanpak:** de getoetste documenten zijn als "
        "bijlage bij dit rapport gevoegd.",
        "",
        "_Dit rapport is opgesteld met ondersteuning van een digitale toetsingsassistent "
        "op basis van het certificatieschema 2024 (Stcrt. 39674), Arbowet, Arbobesluit, "
        "Arboregeling, de Steunpunt RI&E-criteria en relevante NEN-normen. De inhoudelijke "
        "eindverantwoordelijkheid berust bij de ondertekenende gecertificeerde "
        "arbokerndeskundige._",
        "",
    ]

    return "\n".join(d)
