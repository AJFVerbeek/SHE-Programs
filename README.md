# SHE-Programs

Programma's voor **Veiligheid, Gezondheid en Milieu** (Safety, Health & Environment / VGM).

De eerste module is een **RI&E** (Risico-Inventarisatie & -Evaluatie) op basis van
de **Fine & Kinney**-methode, gebouwd met **FastAPI**.

## Risicobeoordeling (Fine & Kinney)

Het risicogetal wordt berekend als:

```
Risico = Waarschijnlijkheid (W) × Blootstelling (B) × Effect (E)
```

| Risicogetal | Klasse        | Actie                                            |
|-------------|---------------|--------------------------------------------------|
| > 400       | Zeer hoog     | Activiteit stoppen; onmiddellijke maatregelen    |
| 200 – 400   | Hoog          | Directe verbetering noodzakelijk                 |
| 70 – 200    | Substantieel  | Maatregelen op korte termijn nodig               |
| 20 – 70     | Mogelijk      | Aandacht vereist; maatregelen overwegen          |
| < 20        | Gering        | Risico acceptabel; monitoren                     |

## Projectstructuur

```
SHE-Programs/
├── app/
│   ├── main.py            # FastAPI-entrypoint
│   ├── config.py          # Instellingen (.env)
│   ├── database.py        # SQLAlchemy engine/sessie
│   ├── scoring.py         # Fine & Kinney-berekening
│   ├── models/            # ORM-modellen (Assessment, Hazard)
│   ├── schemas/           # Pydantic-schema's
│   ├── crud/              # Data-toegangslaag
│   ├── routers/           # API- en web-routes
│   ├── templates/         # Jinja2-templates (webinterface)
│   └── static/            # CSS
├── tests/                 # Pytest-tests
├── requirements.txt
└── .env.example
```

## Installatie

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # optioneel aanpassen
```

## Starten

Snelste manier (maakt automatisch een venv aan, installeert en start):

```bash
./run.sh
```

Of handmatig:

```bash
uvicorn app.main:app --reload
```

- Webinterface: <http://127.0.0.1:8000/>
- API-documentatie (Swagger): <http://127.0.0.1:8000/docs>
- Health-check: <http://127.0.0.1:8000/health>

## Tests

```bash
pytest
```
