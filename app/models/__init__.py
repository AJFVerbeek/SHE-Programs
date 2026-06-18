"""ORM-modellen voor de RI&E- en incidentmodule."""

from app.models.incident import Incident
from app.models.rie import Assessment, Hazard

__all__ = ["Assessment", "Hazard", "Incident"]
