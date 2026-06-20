"""Toetsingscriteria voor de RI&E en het Plan van Aanpak.

De criteria volgen de nummering uit Staatscourant 2024 nr. 39674 (12 december
2024) en de indeling van het vastgestelde AMM-toetssjabloon (v2.2). Enkele
criteria worden conform het sjabloon samengevoegd in één toetsregel:

* 1.1.5 / 1.1.8 / 1.1.9  - preventiemedewerker
* 1.1.6 / 1.1.10         - arbeidsgezondheidskundige onderzoeken
* 1.1.13 / 1.1.14        - risicobeperkende maatregelen + arbeidshygiënische principes
* 1.4.1 / 1.4.2 / 1.4.3  - blootstellingen representatief, gevalideerde methodes, evaluatie correct
"""

from __future__ import annotations

from dataclasses import dataclass

# Toegestane oordelen per toetsregel (volgorde = sjabloonvolgorde).
OORDELEN: tuple[str, ...] = ("Ja", "Deels", "Nee", "n.v.t.")

# RAG-codering van de oordelen conform de AMM-huisstijl.
RAG_KLEUR: dict[str, str] = {
    "Ja": "🟢",
    "Deels": "🟠",
    "Nee": "🔴",
    "n.v.t.": "⚪",
}


@dataclass(frozen=True)
class Criterium:
    """Eén toetsregel: een nummer, een omschrijving en de tabel waarin het hoort."""

    id: str
    tabel: str
    omschrijving: str


# --- Hoofdstuk 1: Toetsen van de RI&E -------------------------------------

VOLLEDIGHEID: tuple[Criterium, ...] = (
    Criterium(
        "1.1.1",
        "1.1 Volledigheid",
        "Zijn alle risico's, inclusief de achterliggende grondoorzaken, ten aanzien "
        "van veiligheid en gezondheid voor de hele organisatie of organisatieonderdelen "
        "(groepen medewerkers of activiteiten) geïnventariseerd?",
    ),
    Criterium(
        "1.1.2",
        "1.1 Volledigheid",
        "Is gebruikgemaakt van verzuimanalyses om inzicht te krijgen in de "
        "arbeidsgerelateerde oorzaken van het verzuim?",
    ),
    Criterium(
        "1.1.3",
        "1.1 Volledigheid",
        "Zijn de inzichten van de bedrijfsarts en andere ingeschakelde deskundigen "
        "voor het verzuim- en arbeidsomstandighedenbeleid meegenomen in de RI&E?",
    ),
    Criterium(
        "1.1.4",
        "1.1 Volledigheid",
        "Zijn de inzichten van de werknemers meegenomen in de RI&E "
        "(medewerkersparticipatie)? Let op: dit is een zwaarwegend criterium.",
    ),
    Criterium(
        "1.1.5 / 1.1.8 / 1.1.9",
        "1.1 Volledigheid",
        "Preventiemedewerker: zijn de inzichten gebruikt, zijn de taken ingevuld en "
        "uitgevoerd, en is beschreven hoeveel preventiemedewerkers nodig zijn met de "
        "benodigde kennis en capaciteit?",
    ),
    Criterium(
        "1.1.6 / 1.1.10",
        "1.1 Volledigheid",
        "Arbeidsgezondheidskundige onderzoeken: zijn de analyses gebruikt in de RI&E "
        "én is beschreven welke onderzoeken nodig zijn, met inhoud en frequentie?",
    ),
    Criterium(
        "1.1.7",
        "1.1 Volledigheid",
        "Zijn ongevallenregistraties aanwezig, geanalyseerd op achterliggende "
        "grondoorzaken en verwerkt in de RI&E?",
    ),
    Criterium(
        "1.1.11",
        "1.1 Volledigheid",
        "Is het arbobeleid beschreven en operationeel?",
    ),
    Criterium(
        "1.1.12",
        "1.1 Volledigheid",
        "Is de organisatie van de bedrijfshulpverlening (BHV) beschreven en operationeel?",
    ),
    Criterium(
        "1.1.13 / 1.1.14",
        "1.1 Volledigheid",
        "Zijn de risicobeperkende maatregelen beschreven én getoetst aan de "
        "arbeidshygiënische principes en het te hanteren redelijkerwijsbeginsel?",
    ),
    Criterium(
        "1.1.15",
        "1.1 Volledigheid",
        "Is bepaald of nadere verdiepende RI&E's en/of aanvullende metingen nodig zijn "
        "om de blootstelling aan arbeidsbelastende factoren vast te stellen?",
    ),
    Criterium(
        "1.1.16",
        "1.1 Volledigheid",
        "Is een basiscontract arbodienstverlening aanwezig dat voldoet aan de "
        "wettelijke minimumeisen (art. 14 Arbowet)?",
    ),
    Criterium(
        "1.1.17",
        "1.1 Volledigheid",
        "Is vastgelegd of de vangnet- of de maatwerkregeling van toepassing is en is "
        "deze correct ingevuld (art. 14/14a Arbowet)?",
    ),
)

ACTUALITEIT: tuple[Criterium, ...] = (
    Criterium(
        "1.2.1",
        "1.2 Actualiteit",
        "Is de RI&E actueel (sluit deze aan op de huidige stand van zaken: gewijzigde "
        "processen, installaties, organisatie en incidenten)?",
    ),
    Criterium(
        "1.2.2",
        "1.2 Actualiteit",
        "Is het Plan van Aanpak actueel en is de actualiteit van RI&E en PvA structureel "
        "geborgd (levend document)?",
    ),
)

ACTUELE_INZICHTEN: tuple[Criterium, ...] = (
    Criterium(
        "1.3.1",
        "1.3 Actuele inzichten",
        "Voldoet de RI&E aan de actuele inzichten, gebaseerd op de stand van de "
        "wetenschap en de professionele dienstverlening (incl. actuele wet- en "
        "regelgeving, normen en grenswaarden)?",
    ),
    Criterium(
        "1.3.2",
        "1.3 Actuele inzichten",
        "Is aantoonbaar gebruikgemaakt van de in de branche opgestelde Arbocatalogus?",
    ),
)

BETROUWBAARHEID: tuple[Criterium, ...] = (
    Criterium(
        "1.4.1 / 1.4.2 / 1.4.3",
        "1.4 Betrouwbaarheid",
        "Zijn de blootstellingen representatief in beeld gebracht (geen over- of "
        "onderschatting), met gevalideerde methodes onderzocht, en is de evaluatie "
        "correct uitgevoerd en vergeleken met relevante wettelijke en wetenschappelijk "
        "onderbouwde grenswaarden?",
    ),
    Criterium(
        "1.4.4",
        "1.4 Betrouwbaarheid",
        "Is het gebruikte RI&E-instrument/de gehanteerde methode valide en passend voor "
        "de organisatie (erkend branche-instrument of gevalideerde methodiek)?",
    ),
)

# --- Hoofdstuk 2: Toetsen van het Plan van Aanpak -------------------------

PLAN_VAN_AANPAK: tuple[Criterium, ...] = (
    Criterium(
        "2.1",
        "2 Plan van Aanpak",
        "Zijn maatregelen voorgesteld om de gevaren weg te nemen of de risico's zoveel "
        "mogelijk te beperken (art. 3 lid 1 Arbowet: verder dan enkel wettelijke normen)?",
    ),
    Criterium(
        "2.2",
        "2 Plan van Aanpak",
        "Is bij de voorstellen voor risicobeperkende maatregelen rekening gehouden met "
        "de arbeidshygiënische strategie en de relevante Arbocatalogus?",
    ),
    Criterium(
        "2.3",
        "2 Plan van Aanpak",
        "Als is afgeweken van de arbeidshygiënische strategie, is dit gemotiveerd?",
    ),
    Criterium(
        "2.4",
        "2 Plan van Aanpak",
        "Is beschreven hoe de maatregelen worden geïmplementeerd?",
    ),
    Criterium(
        "2.5",
        "2 Plan van Aanpak",
        "Is de effectiviteit van de maatregelen ingeschat?",
    ),
    Criterium(
        "2.6",
        "2 Plan van Aanpak",
        "Is rekening gehouden met ongewenste consequenties van de maatregelen?",
    ),
    Criterium(
        "2.7",
        "2 Plan van Aanpak",
        "Is de juiste prioritering van maatregelen voorgesteld op basis van de weging "
        "van de grootte van de risico's?",
    ),
    Criterium(
        "2.8",
        "2 Plan van Aanpak",
        "Is het Plan van Aanpak concreet en realistisch (SMART)?",
    ),
    Criterium(
        "2.9",
        "2 Plan van Aanpak",
        "Hebben de aangewezen actiehouders voldoende bevoegdheid en speelruimte "
        "(geld, tijd) om de maatregelen uit te voeren?",
    ),
    Criterium(
        "2.10",
        "2 Plan van Aanpak",
        "Is het Plan van Aanpak door de directie vastgesteld?",
    ),
)

# Alle RI&E-criteria (hoofdstuk 1) en alle criteria samen.
RIE_CRITERIA: tuple[Criterium, ...] = (
    VOLLEDIGHEID + ACTUALITEIT + ACTUELE_INZICHTEN + BETROUWBAARHEID
)
ALLE_CRITERIA: tuple[Criterium, ...] = RIE_CRITERIA + PLAN_VAN_AANPAK


def criterium_ids() -> list[str]:
    """De id's van alle toetsregels, in sjabloonvolgorde."""
    return [c.id for c in ALLE_CRITERIA]
