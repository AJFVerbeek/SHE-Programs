"""De toetsingsprompt en het uitvoerschema voor de RI&E-toetsing.

Gebaseerd op de vastgestelde AMM-prompt 'Toetsing RI&E' versie 2.2.
"""

from __future__ import annotations

from .criteria import ALLE_CRITERIA, OORDELEN

# Vaste toetsgegevens van de arbokerndeskundige (AKD), conform sectie 1.1.
AKD_GEGEVENS: dict[str, str] = {
    "akd": "Dr. A.J.F. (André) Verbeek",
    "registratienummer": "AKD-65 (Hobeon/SKO reg.nr. 103708-007) — scopes HVK · AH · A&O",
    "organisatie": "AMM Consultancy B.V.",
    "email": "info@ammconsultancy.nl",
    "telefoon": "+31 857 731 716",
    "website": "www.ammconsultancy.nl",
}


def _criteria_blok() -> str:
    """Render de toetsregels als genummerde lijst voor in de systeemprompt."""
    regels = [f"{c.id} ({c.tabel}): {c.omschrijving}" for c in ALLE_CRITERIA]
    return "\n".join(regels)


SYSTEEMPROMPT = f"""\
Je bent een gecertificeerde ArboKernDeskundige (AKD) van AMM Consultancy B.V.,
gecertificeerd voor de scopes Hogere Veiligheidskunde (HVK), Arbeidshygiëne (AH)
en Arbeids- en Organisatiedeskundige (A&O). Je toetst een Risico-Inventarisatie
& -Evaluatie (RI&E) met bijbehorend Plan van Aanpak (PvA) en stelt een compleet
Toets- en adviesrapport op.

Wettelijke basis:
- Arbowet artikel 5 (RI&E-verplichting), artikel 13 (deskundige bijstand),
  artikel 14 en 14a (maatwerk- en vangnetregeling).
- Staatscourant 2024 nr. 39674 (12 december 2024) — toetsingscriteria RI&E.
- Staatscourant 2022 nr. 7980 (16 maart 2022) — Arboregeling.

Toetsgegevens AKD:
- AKD: {AKD_GEGEVENS["akd"]}
- Registratie: {AKD_GEGEVENS["registratienummer"]}
- Adviesbureau: {AKD_GEGEVENS["organisatie"]} ({AKD_GEGEVENS["email"]}, {AKD_GEGEVENS["telefoon"]})

Toets de aangeleverde documenten systematisch aan elk van onderstaande
toetsregels. Geef per toetsregel een oordeel ({" / ".join(OORDELEN)}), een
onderbouwde bevinding en een concreet advies.

TOETSREGELS:
{_criteria_blok()}

Beoordelingsregels:
- Medewerkersparticipatie (1.1.4) is zwaarwegend: weeg dit expliciet mee, ook in
  de samenvatting.
- Controleer bestaande adviezen in de RI&E/PvA op adequaatheid en geef aan of ze
  aanvulling behoeven.
- Houd rekening met de relevante branche; benoem branchespecifieke risico's.
- Beschrijf welke verdiepende onderzoeken nog uitgevoerd dienen te worden
  (bijv. PSA/MTO, fysieke belasting, gevaarlijke stoffen, biologische agentia,
  geluid, trillingen).
- Geef bij twijfel expliciet aan waar onzekerheid bestaat en kies dan 'Deels'.
- Gebruik de terminologie 'Kinney & Wiruth', nooit 'Fine-Kinney'.

Lever uitsluitend het gevraagde JSON-object op, zonder extra tekst. Schrijf alle
inhoud in het Nederlands.
"""

# JSON-schema voor de gestructureerde uitvoer (output_config.format).
UITVOER_SCHEMA: dict = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "organisatieprofiel": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "organisatienaam": {"type": "string"},
                "branche_sbi": {"type": "string"},
                "aantal_medewerkers": {"type": "string"},
                "datum_rie": {"type": "string"},
                "gebruikt_instrument": {"type": "string"},
                "toetsingsdatum": {"type": "string"},
            },
            "required": [
                "organisatienaam",
                "branche_sbi",
                "aantal_medewerkers",
                "datum_rie",
                "gebruikt_instrument",
                "toetsingsdatum",
            ],
        },
        "toetsingen": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "oordeel": {"type": "string", "enum": list(OORDELEN)},
                    "bevinding": {"type": "string"},
                    "advies": {"type": "string"},
                },
                "required": ["id", "oordeel", "bevinding", "advies"],
            },
        },
        "oordeel_volledigheid": {"type": "string"},
        "oordeel_actualiteit": {"type": "string"},
        "oordeel_betrouwbaarheid": {"type": "string"},
        "advies_plan_van_aanpak": {"type": "string"},
        "verdiepende_onderzoeken": {"type": "array", "items": {"type": "string"}},
        "scope_ah": {"type": "string"},
        "scope_hvk": {"type": "string"},
        "scope_ao": {"type": "string"},
        "samenvatting": {"type": "string"},
    },
    "required": [
        "organisatieprofiel",
        "toetsingen",
        "oordeel_volledigheid",
        "oordeel_actualiteit",
        "oordeel_betrouwbaarheid",
        "advies_plan_van_aanpak",
        "verdiepende_onderzoeken",
        "scope_ah",
        "scope_hvk",
        "scope_ao",
        "samenvatting",
    ],
}
