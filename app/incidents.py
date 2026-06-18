"""Vaste keuzelijsten (enums) voor de incidentregistratie."""

from enum import StrEnum


class IncidentType(StrEnum):
    """Soort melding."""

    ONGEVAL = "Ongeval"
    BIJNA_ONGEVAL = "Bijna-ongeval"
    ONVEILIGE_SITUATIE = "Onveilige situatie"
    MILIEU_INCIDENT = "Milieu-incident"


class Severity(StrEnum):
    """Ernst van het incident."""

    GEEN_LETSEL = "Geen letsel"
    EHBO = "Licht letsel (EHBO)"
    VERZUIM = "Letsel met verzuim"
    ERNSTIG = "Ernstig letsel"
    DODELIJK = "Dodelijk"


class IncidentStatus(StrEnum):
    """Afhandelingsstatus."""

    OPEN = "Open"
    IN_BEHANDELING = "In behandeling"
    AFGEHANDELD = "Afgehandeld"
