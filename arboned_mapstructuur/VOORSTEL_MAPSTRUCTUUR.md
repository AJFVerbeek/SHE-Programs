# Voorstel mapstructuur — P176_2 ArboNed Toetsingen

*Opgesteld: 21 juli 2026*

Dit voorstel is gebaseerd op een analyse van de huidige inhoud van
`General/3. Uitvoering/P176_2 Arboned Toetsingen` op SharePoint/OneDrive.

---

## 1. Huidige situatie

De hoofdmap bevat op dit moment op één niveau, door elkaar:

| Type | Voorbeelden | Omvang |
|---|---|---|
| Actieve klantdossiers | `65. Ratu Culinair (Marcel)` t/m `538. Liliane Fonds PSA (Ray)` | ± 20 mappen |
| Procesmappen (AI-werkstroom) | `1a Input`, `2a. Beoordeeld`, `3a Output`, `4a Output Toetsrapporten` | ± 1,4 GB |
| Archief | `Uitgevoerd Toetsingen` (± 285 afgeronde dossiers) | ± 8,6 GB |
| Sjablonen | `0. Sjablonen` (met o.a. 8 submappen en ± 30 losse bestanden) | 10 MB |
| Beheer | `0.0 Uren`, `0.0.0 Diverse`, `0000. Verzonden items` | 24 MB |
| Enquêtes | `Enquetes` én `2b. PSA-enquetes` (twee mappen, zelfde onderwerp) | 28 MB |
| Overig | `AKD-Eindrapporten mei 2026`, `524 Bespreking A&O-ers`, losse bestanden (`.ico`, `Intake-uitvraag_KOH-etsruimte.docx`) | |

### Knelpunten

1. **Twee nummerreeksen door elkaar** — het archief (`Uitgevoerd Toetsingen`) nummert 1–285, de actieve dossiers in de hoofdmap nummeren 65–538. Nummers overlappen (bijv. 145, 149 komen in beide reeksen voor), waardoor zoeken op nummer onbetrouwbaar is.
2. **Proces- en dossiermappen op hetzelfde niveau** — `1a Input` staat alfabetisch tussen klant 194 en 216 in; je moet de hele lijst scannen om iets te vinden.
3. **Inconsistente naamgeving** — `247. Pirtek (Aad)`, `503 Conveni` (geen punt), `127.Welcome` (geen spatie), `178. Lutscher Alm Hans-v)` (haakje weggevallen), nummer `260` komt twee keer voor.
4. **Sjablonen zonder versiebeheer** — `v7`, `v7.1`, `v7.1 - kopie` en `Template-X3` staan naast elkaar; niet zichtbaar welke actueel is.
5. **Dubbele/vage verzamelmappen** — `Enquetes` naast `2b. PSA-enquetes`; `0.0.0 Diverse` en `0000. Verzonden items` met kunstmatige nulnummering om bovenaan te sorteren.
6. **Losse bestanden in de hoofdmap** — o.a. een `.ico`-bestand en een intake-document zonder dossier.
7. **Onduidelijke rol van `3a Output`** — deze map is leeg; output staat in `4a Output Toetsrapporten`.

---

## 2. Voorgestelde structuur

Uitgangspunten: maximaal **7 hoofdmappen**, elk met een vast nummer zodat de
volgorde de werkstroom volgt; klantdossiers alleen op één plek (lopend óf
afgerond); en één nummerreeks voor alle dossiers.

```
P176_2 ArboNed Toetsingen/
│
├── 0_Beheer/
│   ├── Uren/                        (was: 0.0 Uren)
│   ├── Correspondentie/             (was: 0000. Verzonden items)
│   ├── Overleg A&O-ers/             (was: 524 Bespreking A&O-ers)
│   └── Diversen/                    (was: 0.0.0 Diverse — daarna opschonen)
│
├── 1_Sjablonen/
│   ├── Toetsrapport/                (alléén de actuele versie)
│   ├── Prompts/                     (was: 1. Claud-RIE-prompt, 2. Claud-PSA-prompt, 4. Claud-autom, …)
│   ├── Enquete/                     (was: 8. Sjabloon-enquete)
│   ├── Logo en huisstijl/
│   └── _Oude versies/               (v7, v7.1, kopieën — niet weggooien, wel uit zicht)
│
├── 2_Lopende dossiers/
│   ├── 503 Conveni (…)/
│   ├── 525 Synthos (Andre)/
│   ├── 538 Liliane Fonds PSA (Ray)/
│   └── …                            (elke map met vaste submappen, zie §3)
│
├── 3_AI-pijplijn/
│   ├── 1_Input/                     (was: 1a Input)
│   ├── 2_Beoordeeld/                (was: 2a. Beoordeeld, incl. _v4builder en memory)
│   └── 3_Toetsrapporten/            (was: 4a Output Toetsrapporten; 3a Output vervalt — is leeg)
│
├── 4_Enquetes/
│   └── (samenvoeging van "Enquetes" en "2b. PSA-enquetes")
│
├── 5_Afgeronde dossiers/
│   └── (was: "Uitgevoerd Toetsingen" — inhoud ongewijzigd laten, alleen de hoofdmap hernoemen)
│
└── 6_Naslag/
    ├── (memo's, wetgeving, BRF/Tripod-documenten uit 0. Sjablonen die geen sjabloon zijn)
    └── AKD-Eindrapporten mei 2026/
```

### Waarom deze indeling

- **De nummering 0–6 volgt de werkstroom**: beheer en sjablonen bovenaan, dan het lopende werk, dan de pijplijn, dan het archief. Geen kunstgrepen als `0.0.0` of `0000.` meer nodig.
- **Klantdossiers staan op precies één plek.** Een dossier leeft in `2_Lopende dossiers` en verhuist na afronding integraal naar `5_Afgeronde dossiers`. De hoofdmap blijft daardoor klein en overzichtelijk (nu ± 40 items, straks 7).
- **Het archief blijft ongemoeid.** De 285 afgeronde dossiers hoeven niet hernoemd of verplaatst te worden; alleen de bovenliggende map krijgt een nieuwe naam. Dat houdt de migratie klein en risicoloos (verplaatsen binnen dezelfde drive is een metadata-operatie, geen kopieerslag van 8,6 GB).
- **`_Oude versies` met underscore-prefix** sorteert onderaan en maakt in één oogopslag duidelijk wat níet de actuele sjabloonversie is.

---

## 3. Vaste submapindeling per dossier

Elk nieuw dossier in `2_Lopende dossiers` krijgt dezelfde vier submappen:

```
NNN Klantnaam (Adviseur)/
├── 1_Input/          (aangeleverde RI&E, PvA, beleidsdocumenten, mailverzoek)
├── 2_Beoordeling/    (werkbestanden, AI-output, transcripten, aantekeningen)
├── 3_Rapport/        (concept- en definitief toets- en adviesrapport)
└── 4_Verzonden/      (wat daadwerkelijk naar ArboNed/klant is gestuurd, als PDF)
```

Zo is per dossier altijd duidelijk wat binnenkwam, wat eraan gedaan is en wat
de deur uit ging — ook jaren later nog.

---

## 4. Naamgevingsafspraken

| Onderwerp | Afspraak | Voorbeeld |
|---|---|---|
| Dossiermap | `NNN Klantnaam (Adviseur)` — driecijferig nummer, spatie, geen punt | `525 Synthos (Andre)` |
| Nummerreeks | Eén doorlopende reeks; het eerstvolgende vrije nummer boven het hoogste bestaande (nu: 539) | `539 Nieuwe Klant (…)` |
| Bestanden met datum | `JJJJMMDD Beschrijving.ext` — sorteert chronologisch | `20260626 Mail verzoek toetsing.pdf` |
| Sjablonen | Naam + versienummer, oude versie direct naar `_Oude versies` | `Toets- en adviesrapport RIE v7.1.docx` |
| Verboden tekens | Geen dubbele spaties, geen punt achter het nummer, haakjes altijd in paren | — |

---

## 5. Migratieplan (stapsgewijs, laag risico)

Voer de migratie uit in de **lokaal gesynchroniseerde OneDrive-map** (Verkenner),
niet via de webinterface — dan blijven de bestandshistorie en gedeelde koppelingen
behouden en gaat het verplaatsen vrijwel direct.

| Stap | Actie | Tijd |
|---|---|---|
| 1 | Draai `Maak-Mapstructuur.ps1` (zie hiernaast) — maakt het lege raamwerk aan naast de bestaande mappen | 1 min |
| 2 | Hernoem `Uitgevoerd Toetsingen` → `5_Afgeronde dossiers` | 1 min |
| 3 | Versleep `1a Input`, `2a. Beoordeeld`, `4a Output Toetsrapporten` naar `3_AI-pijplijn` en hernoem ze; verwijder de lege map `3a Output` | 5 min |
| 4 | Versleep de actieve klantdossiers (65 t/m 538) naar `2_Lopende dossiers`; corrigeer daarbij meteen de naamgeving | 15 min |
| 5 | Verdeel `0. Sjablonen`: actuele sjablonen naar `1_Sjablonen`, oude versies naar `1_Sjablonen/_Oude versies`, naslagdocumenten (memo's, BRF, wetgeving) naar `6_Naslag` | 30 min |
| 6 | Voeg `Enquetes` en `2b. PSA-enquetes` samen in `4_Enquetes` | 10 min |
| 7 | Verplaats `0.0 Uren`, `0000. Verzonden items`, `524 Bespreking A&O-ers` en `0.0.0 Diverse` naar `0_Beheer` | 5 min |
| 8 | Ruim de losse bestanden in de hoofdmap op (`.ico` verwijderen; `Intake-uitvraag_KOH-etsruimte.docx` naar het bijbehorende dossier) | 5 min |
| 9 | Controle: de hoofdmap bevat nu alleen de mappen 0 t/m 6 | 2 min |

**Totaal: ruim een uur.** Er wordt niets weggegooid (behalve de lege map `3a Output`
en het `.ico`-bestand); alles wordt alleen verplaatst of hernoemd. Bij twijfel over
een bestand: in `0_Beheer/Diversen` zetten en later beoordelen.

### Tip voor daarna

Maak in `1_Sjablonen` een leeg dossiersjabloon `_Nieuw dossier NNN Klantnaam (Adviseur)`
met de vier submappen uit §3. Een nieuw dossier starten is dan: kopiëren en hernoemen.
Het script `Nieuw-Dossier.ps1` doet dit automatisch.
