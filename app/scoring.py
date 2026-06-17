"""Fine & Kinney-risicobeoordeling voor de RI&E.

Het risicogetal wordt berekend als::

    Risico = Waarschijnlijkheid (W) x Blootstelling (B) x Effect (E)

De toegestane waarden voor W, B en E liggen vast in onderstaande schalen,
conform de Fine & Kinney-methode.
"""

from dataclasses import dataclass

# Toegestane waarden per factor (Fine & Kinney).
PROBABILITY_VALUES: tuple[float, ...] = (0.1, 0.2, 0.5, 1, 3, 6, 10)
EXPOSURE_VALUES: tuple[float, ...] = (0.5, 1, 2, 3, 6, 10)
EFFECT_VALUES: tuple[float, ...] = (1, 3, 7, 15, 40, 100)


@dataclass(frozen=True)
class RiskClass:
    """Een risicoklasse met ondergrens en geadviseerde actie."""

    label: str
    action: str


# Klassen gesorteerd van hoog naar laag op ondergrens (exclusief).
_RISK_BANDS: tuple[tuple[float, RiskClass], ...] = (
    (400, RiskClass("Zeer hoog", "Activiteit stoppen; onmiddellijke maatregelen vereist")),
    (200, RiskClass("Hoog", "Directe verbetering noodzakelijk")),
    (70, RiskClass("Substantieel", "Maatregelen op korte termijn nodig")),
    (20, RiskClass("Mogelijk", "Aandacht vereist; maatregelen overwegen")),
    (0, RiskClass("Gering", "Risico acceptabel; monitoren")),
)


def _validate(value: float, allowed: tuple[float, ...], name: str) -> None:
    if value not in allowed:
        raise ValueError(
            f"{name} moet een van {allowed} zijn, kreeg {value!r}."
        )


def calculate_risk_score(probability: float, exposure: float, effect: float) -> float:
    """Bereken het Fine & Kinney-risicogetal (W x B x E).

    Raises:
        ValueError: als een van de factoren buiten de toegestane schaal valt.
    """
    _validate(probability, PROBABILITY_VALUES, "Waarschijnlijkheid")
    _validate(exposure, EXPOSURE_VALUES, "Blootstelling")
    _validate(effect, EFFECT_VALUES, "Effect")
    return round(probability * exposure * effect, 2)


def classify_risk(score: float) -> RiskClass:
    """Bepaal de risicoklasse op basis van het risicogetal."""
    for lower_bound, risk_class in _RISK_BANDS:
        if score > lower_bound:
            return risk_class
    # score == 0
    return _RISK_BANDS[-1][1]
