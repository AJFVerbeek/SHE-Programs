# RI&E-toets-tool (AMM Consultancy)

Toetst een **Risico-Inventarisatie & -Evaluatie (RI&E)** met bijbehorend **Plan
van Aanpak** aan de wettelijke toetsingscriteria en genereert een compleet
**Toets- en adviesrapport** conform het vastgestelde AMM-sjabloon (v2.2).

De tool giet de vastgestelde AMM-toetsworkflow in code: documenten inlezen →
systematisch toetsen via de Claude API → rapport opbouwen.

## Wettelijk kader

- Arbowet artikel 5, 13, 14 en 14a
- Toetsingscriteria RI&E — **Staatscourant 2024 nr. 39674** (12 december 2024)
- Arboregeling — Staatscourant 2022 nr. 7980

De toetsregels (1.1.1 t/m 1.4.4 voor de RI&E en 2.1 t/m 2.10 voor het Plan van
Aanpak) staan in [`rie_toetsing/criteria.py`](rie_toetsing/criteria.py), met de
in het sjabloon voorgeschreven samenvoegingen.

> Terminologie: **Kinney & Wiruth** (nooit "Fine-Kinney").

## Wat de tool doet

1. **Inlezen** van RI&E, Plan van Aanpak en eventuele bijlagen
   (`.pdf`, `.docx`, `.txt`, `.md`). PDF's gaan rechtstreeks naar het model.
2. **Toetsen** van elke toetsregel: oordeel (Ja / Deels / Nee / n.v.t.),
   bevinding en advies, plus oordelen op volledigheid, actualiteit en
   betrouwbaarheid, een advies op het Plan van Aanpak, verdiepende onderzoeken
   en een samenvatting per scope (AH / HVK / A&O).
3. **Rapport** genereren als Markdown volgens de sjabloonstructuur, met
   RAG-codering (🟢 Ja · 🟠 Deels · 🔴 Nee · ⚪ n.v.t.).
4. Optioneel **branche-onderzoek** via web search vooraf (`--branche-onderzoek`).

## Installatie

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env               # vul ANTHROPIC_API_KEY in
```

## Gebruik

```bash
# Volledige toetsing, rapport als Markdown
rie-toets RIE.pdf --pva PlanVanAanpak.pdf --org "Voorbeeld B.V." \
    --output toetsrapport.md

# Rapport als Word-document in AMM-huisstijl (.docx → automatisch docx)
rie-toets RIE.pdf --pva PlanVanAanpak.pdf --org "Voorbeeld B.V." \
    --output toetsrapport.docx

# Met branche-onderzoek vooraf
rie-toets RIE.pdf --pva PvA.pdf --org "Voorbeeld B.V." --branche "43.99" \
    --branche-onderzoek -o rapport.docx

# Leeg sjabloon zonder API-aanroep
rie-toets RIE.pdf --dry-run -o sjabloon.docx
```

Belangrijkste opties: `--pva`, `--bhv`, `--arbobeleid`, `--verdiepend`
(allemaal herhaalbaar), `--org`, `--branche`, `--branche-onderzoek`,
`--model`, `--output/-o`, `--format {md,docx}`, `--dry-run`.

### Uitvoerformaat

- **Markdown** (`.md`, standaard) — snel te lezen en te versioneren.
- **Word** (`.docx`) — in de AMM-huisstijl: primair blauw `#5467B0`, Aptos,
  voorpagina en samenvatting staand, tabelpagina's liggend, en RAG-gekleurde
  oordeelcellen (🟢 Ja · 🟠 Deels · 🔴 Nee · ⚪ n.v.t.) met een wit vinkje.

Het formaat wordt afgeleid van de extensie van `--output`, of expliciet gekozen
met `--format`.

## Tests

```bash
pip install pytest
pytest
```

De tests voor de criteria en de rapportgenerator draaien volledig offline
(geen API-sleutel nodig).

## Verantwoordelijkheid

Dit rapport wordt opgesteld met ondersteuning van een digitale toetsingsassistent.
De inhoudelijke eindverantwoordelijkheid berust bij de ondertekenende
gecertificeerde arbokerndeskundige (AKD).
