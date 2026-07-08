# Backlog — RI&E-toets-tool (AMM Consultancy)

Overzicht van mogelijk vervolgwerk voor de RI&E-toets-tool, geprioriteerd
volgens MoSCoW (**Moet** / **Zou** / **Kan** / **Later**). Peildatum: 2026-06-20.

## Status van vandaag

De tool is werkend en staat op `main`: RI&E + Plan van Aanpak toetsen aan de
criteria (Stcrt. 2024 nr. 39674), rapport in Markdown of Word (AMM-huisstijl,
optioneel op basis van het AMM-sjabloon), CLI met begeleide Windows-startscripts,
handleiding en 13 offline tests. De **live toetsing via de Claude API** is nog
niet end-to-end geverifieerd met een echte RI&E.

## Geprioriteerde backlog

| ID | Prioriteit | Onderdeel | Beschrijving | Status |
|---|---|---|---|---|
| B1 | Moet | Live verificatie | Eén echte RI&E + Plan van Aanpak toetsen met API-sleutel; oordelen, bevindingen en advies controleren op inhoud. | Open |
| B2 | Moet | AMM-sjabloon valideren | De export testen met het échte `AMM_..._SJABLOON_v2.2.docx`: logo, marges, koptekst, voettekst en paginanummering. | Open |
| B3 | Moet | Kwaliteitscontrole oordelen | Steekproef: kloppen de oordelen (Ja/Deels/Nee/n.v.t.) en verwijzen adviezen naar de juiste artikelen/normen? | Open |
| B4 | Zou | Hertoetsing ontbrekende regels | Als een toetsregel geen oordeel kreeg, gericht opnieuw laten beoordelen i.p.v. de hele toetsing. | Open |
| B5 | Zou | Verdiepende onderzoeken (Bijlage 1) | Per organisatie automatisch markeren welke verdiepende onderzoeken relevant zijn conform Stcrt. 2024-39674. | Open |
| B6 | Zou | Tweede-lezing (adversarial) | Oordelen laten verifiëren door een tweede modelronde die tegenspraak zoekt, vóór opname in het rapport. | Open |
| B7 | Zou | Batch-toetsing | Meerdere RI&E's in één keer toetsen (map met documenten) met overzichtsrapport. | Open |
| B8 | Zou | Kostenraming vooraf | Tokentelling en geschatte kosten tonen vóór de toetsing start. | Open |
| B9 | Zou | AKD-gegevens configureerbaar | AKD-naam, registratie en contact via `.env`/config i.p.v. in de code. | Open |
| B10 | Zou | `.doc` ondersteunen | Ook oud Word-formaat (`.doc`) kunnen inlezen, naast `.pdf`/`.docx`/`.txt`/`.md`. | Open |
| B11 | Kan | Grafische interface | Eenvoudige GUI (venster met knoppen) i.p.v. de opdrachtregel. | Open |
| B12 | Kan | Export naar PDF | Rapport ook als PDF kunnen opleveren. | Open |
| B13 | Kan | SharePoint-koppeling | Documenten rechtstreeks uit SharePoint ophalen en rapport terugplaatsen. | Open |
| B14 | Kan | Tests uitbreiden | Tests voor `documenten.py` en `toetser.py` (met gemockte API). | Open |
| B15 | Kan | CI (GitHub Actions) | Automatisch de tests draaien bij elke wijziging. | Open |
| B16 | Kan | Afhankelijkheden vastzetten | Versies pinnen/lockfile voor reproduceerbare installatie. | Open |
| B17 | Kan | Logging en audit | Toetsingen loggen (wanneer, welk document, welk model) voor traceerbaarheid. | Open |
| B18 | Later | Integratie SHE-app | Koppelen aan de bestaande FastAPI-RI&E-app (branch `verhip-integration`). | Open |

## Bekende beperkingen

- De live toetsing is afhankelijk van een geldige `ANTHROPIC_API_KEY` en
  internettoegang.
- De Word-export bouwt de toetstabellen opnieuw op; alleen de sjabloon-onderdelen
  (logo, kop-/voettekst, marges) worden overgenomen, niet de exacte
  tabelopmaak van het sjabloon.
- Terminologie is vastgezet op **Kinney & Wiruth**; de tool is uitsluitend
  Nederlandstalig.
- De inhoudelijke eindverantwoordelijkheid berust altijd bij de gecertificeerde
  arbokerndeskundige (AKD).

## Notities

- Prioriteiten zijn een voorstel; pas ze aan op basis van de eerste echte
  toetsing (B1) en de sjabloon-validatie (B2).
- Nieuwe wensen kunnen als extra regel (B19, B20, …) worden toegevoegd.
