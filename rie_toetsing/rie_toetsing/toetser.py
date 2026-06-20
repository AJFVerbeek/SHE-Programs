"""Aansturing van de Claude API voor de RI&E-toetsing.

De toetsing draait in twee stappen:

1. (optioneel) een branche-onderzoek via web search dat aanvullende context
   over de organisatie en branchespecifieke risico's verzamelt;
2. de eigenlijke toetsing, die de documenten aan de toetscriteria toetst en een
   gestructureerd resultaat teruggeeft.
"""

from __future__ import annotations

import json
from typing import Any

from .documenten import Document, naar_contentblokken
from .prompt import SYSTEEMPROMPT, UITVOER_SCHEMA

# Standaardmodel: het meest capabele Claude-model.
STANDAARD_MODEL = "claude-opus-4-8"


def _client(api_key: str | None = None):
    """Maak een Anthropic-client (lazy import zodat de rest zonder SDK werkt)."""
    try:
        import anthropic  # type: ignore
    except ImportError as exc:  # pragma: no cover - afhankelijk van omgeving
        raise RuntimeError(
            "De 'anthropic' SDK is nodig: pip install anthropic"
        ) from exc
    return anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()


def onderzoek_branche(
    organisatie: str,
    branche: str = "",
    *,
    model: str = STANDAARD_MODEL,
    api_key: str | None = None,
) -> str:
    """Verzamel via web search aanvullende context over organisatie en branche."""
    client = _client(api_key)
    vraag = (
        f"Zoek beknopte, actuele context voor een RI&E-toetsing van de organisatie "
        f"'{organisatie}'"
        + (f" (branche: {branche})" if branche else "")
        + ". Geef: de relevante SBI-code/branche, of er een erkende branche-RI&E en "
        "Arbocatalogus bestaat, en de belangrijkste branchespecifieke arbeidsrisico's. "
        "Vat bondig samen in het Nederlands."
    )
    with client.messages.stream(
        model=model,
        max_tokens=4000,
        thinking={"type": "adaptive"},
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[{"role": "user", "content": vraag}],
    ) as stream:
        bericht = stream.get_final_message()

    return "".join(b.text for b in bericht.content if getattr(b, "type", None) == "text")


def toets(
    documenten: list[Document],
    *,
    organisatie: str = "",
    branche_context: str = "",
    model: str = STANDAARD_MODEL,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Toets de documenten aan de criteria en geef het gestructureerde resultaat.

    Returns:
        Het JSON-object volgens :data:`prompt.UITVOER_SCHEMA`.
    """
    if not documenten:
        raise ValueError("Er zijn geen documenten om te toetsen.")

    client = _client(api_key)

    inleiding = "Toets de bijgevoegde documenten aan de toetscriteria."
    if organisatie:
        inleiding += f" Organisatie: {organisatie}."
    if branche_context:
        inleiding += f"\n\nAanvullende branche-context:\n{branche_context}"

    content: list[dict] = [{"type": "text", "text": inleiding}]
    content.extend(naar_contentblokken(documenten))

    with client.messages.stream(
        model=model,
        max_tokens=32000,
        thinking={"type": "adaptive"},
        output_config={
            "effort": "high",
            "format": {"type": "json_schema", "schema": UITVOER_SCHEMA},
        },
        system=SYSTEEMPROMPT,
        messages=[{"role": "user", "content": content}],
    ) as stream:
        bericht = stream.get_final_message()

    if bericht.stop_reason == "refusal":
        raise RuntimeError(
            "De toetsing is geweigerd door de veiligheidsclassificatie van het model."
        )

    tekst = next(
        (b.text for b in bericht.content if getattr(b, "type", None) == "text"), ""
    )
    return json.loads(tekst)
