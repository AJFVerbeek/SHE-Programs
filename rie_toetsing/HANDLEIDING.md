# Handleiding — een RI&E toetsen

Stap-voor-stap, ook zonder programmeerkennis. De installatie is eenmalig;
daarna is een RI&E toetsen telkens één commando.

---

## Deel A — Eenmalig instellen

### 1. Python controleren

Open een terminal (macOS: *Terminal*, Windows: *PowerShell*) en typ:

```bash
python --version
```

Zie je `Python 3.11` of hoger? Ga door. Zo niet, installeer Python via
<https://www.python.org/downloads/> (vink bij Windows **"Add Python to PATH"** aan).

### 2. De code ophalen

```bash
git clone https://github.com/AJFVerbeek/SHE-Programs.git
cd SHE-Programs
git checkout claude/rie-toetsen-code-sjnq6s
cd rie_toetsing
```

### 3. De tool installeren

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
```

> Let op: telkens als je een nieuwe terminal opent, eerst weer
> `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) draaien.

### 4. Je Claude API-sleutel instellen

```bash
cp .env.example .env
```

Open `.env` en zet je sleutel erin:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Activeer hem in de huidige terminal:

```bash
export ANTHROPIC_API_KEY=sk-ant-...     # Windows: set ANTHROPIC_API_KEY=sk-ant-...
```

### 5. Controleren of alles staat (geen sleutel nodig)

```bash
rie-toets --version
```

Krijg je een versienummer te zien (bijv. `rie-toets 0.1.0`), dan is de
installatie gelukt.

---

## Deel B — Een RI&E toetsen

### 6. Toetsing draaien

Zet je RI&E (en eventueel het Plan van Aanpak) klaar en draai:

```bash
rie-toets RIE.pdf --pva PlanVanAanpak.pdf --org "Naam B.V." -o toetsrapport.docx
```

- `RIE.pdf` — pad naar je RI&E (`.pdf`, `.docx`, `.txt` of `.md`)
- `--pva` — pad naar het Plan van Aanpak (optioneel)
- `--org` — naam van de organisatie
- `-o toetsrapport.docx` — naam van het uitvoerbestand

De tool leest de documenten in, toetst elke toetsregel via de Claude API en
schrijft het rapport. Dit duurt doorgaans één tot enkele minuten.

### 7. Het rapport openen

Open `toetsrapport.docx` in Word. Je vindt er:

- voorpagina, samenvatting en basisgegevens;
- per toetsregel het oordeel met kleurcodering — 🟢 Ja · 🟠 Deels · 🔴 Nee ·
  ⚪ n.v.t. — plus bevinding en advies;
- samenvatting per scope (AH / HVK / A&O);
- toetsing van het Plan van Aanpak en de afronding.

---

## Deel C — Handige varianten

| Wil je… | Voeg toe |
|---|---|
| Eerst kijken zónder de API te gebruiken (leeg sjabloon) | `--dry-run` |
| Branche-info automatisch laten opzoeken | `--branche-onderzoek --branche "43.99"` |
| Het rapport als Markdown i.p.v. Word | `-o toetsrapport.md` |
| Het AMM-sjabloon (logo, marges, voettekst) gebruiken | `--sjabloon AMM_...SJABLOON_v2.2.docx` |
| BHV-plan en arbobeleid meenemen | `--bhv BHV.pdf --arbobeleid Beleid.pdf` |
| Verdiepend onderzoek meenemen | `--verdiepend PSA.pdf` |
| Alle opties zien | `rie-toets --help` |

**Snelle controle dat alles werkt** (zonder API-sleutel, levert een leeg
sjabloon):

```bash
rie-toets RIE.pdf --org "Test B.V." --dry-run -o test.docx
```

Komt er een `test.docx` uit, dan staat de tool goed en is alleen nog je
API-sleutel nodig voor de inhoud.

---

## Veelgestelde vragen

**"rie-toets: command not found"**
Je `.venv` is niet geactiveerd. Draai eerst
`source .venv/bin/activate` (Windows: `.venv\Scripts\activate`).
Als alternatief werkt altijd: `python -m rie_toetsing.cli ...`.

**"De 'anthropic' SDK is nodig"**
Voer `pip install -e .` uit in de map `rie_toetsing`.

**"Fout tijdens toetsing" / authenticatiefout**
Controleer of `ANTHROPIC_API_KEY` is ingesteld in dezelfde terminal.

**Wat als een toetsregel geen oordeel kreeg?**
De tool meldt dit onderaan in de terminal. Controleer of de RI&E het
betreffende onderwerp bevat, of draai opnieuw.

---

## Belangrijk

Dit rapport wordt opgesteld met ondersteuning van een digitale toetsingsassistent.
De inhoudelijke **eindverantwoordelijkheid** berust bij de ondertekenende
gecertificeerde arbokerndeskundige (AKD). Lees het rapport altijd na en pas waar
nodig aan vóór ondertekening en verzending aan OR/PVT.
