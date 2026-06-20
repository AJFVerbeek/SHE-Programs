# Test Coverage Analysis — SHE-Programs

> Scope note: the application code lives on branch
> `claude/verhip-integration-a6qnae` (FastAPI app for RI&E risk assessments
> and incident registration). `main` currently contains only the README.
> This report was produced by running the existing suite against that branch.

## How this was measured

```bash
pip install -r requirements.txt pytest-cov
python -m pytest --cov=app --cov-report=term-missing
```

**Result: 31 tests pass, 88% total line coverage.**

| Module | Stmts | Miss | Cover | Notable missing |
|---|---:|---:|---:|---|
| app/routers/web.py | 79 | 36 | **54%** | RI&E web UI: create/rename/add-hazard/edit/delete forms, helpers |
| app/database.py | 13 | 4 | 69% | real `get_db` (overridden in tests) |
| app/routers/incident_web.py | 42 | 11 | 74% | incident detail/edit/delete web forms |
| app/routers/api.py | 51 | 9 | 82% | list & delete assessment, `add_hazard` ValueError branch |
| app/pdf.py | 46 | 4 | 91% | empty-assessment ("geen gevaren") branch |
| app/crud/rie.py | 47 | 3 | 94% | `list_assessments`, `delete_assessment` |
| app/main.py | 18 | 1 | 94% | `/health` |
| app/routers/incident_api.py | 30 | 1 | 97% | delete 404 |
| app/scoring.py | 22 | 0 | 100%* | *line-covered, but band-edge values untested |
| schemas/*, models/*, incidents.py, config.py | — | 0 | 100% | — |
| **TOTAL** | **568** | **69** | **88%** | |

The headline 88% hides the real risk: it is concentrated in the
server-rendered web layer and in branch/value gaps that line coverage
cannot see.

## Priority areas to improve

### P1 — RI&E web routes (`routers/web.py`, 54%)
The largest module is almost untested; only the PDF endpoint is covered.
Untested: `GET /` (index), `POST /assessments`, `GET /assessments/{id}`
(detail render), `/rename`, `POST .../hazards`, `GET`/`POST /hazards/{id}/edit`,
`POST /hazards/{id}/delete`, plus helpers `_safe_filename`, `_optional_float`,
`_hazard_from_form`. These routes are the only place the `index`, `detail`
and `hazard_edit` Jinja templates are rendered — a broken template would
ship undetected.
- Add form-flow tests (`follow_redirects=True`) like `test_web_incidents_pages`.
- Unit-test `_safe_filename` (special chars, empty → `"rie"`) and
  `_optional_float` (`""`/whitespace → `None`).

### P2 — Classification band edges (`scoring.classify_risk`)
`scoring.py` is 100% line-covered yet the strict `score > lower_bound`
comparison means the exact edges — **20, 70, 200, 400** — are the most
off-by-one-prone and are never asserted. Add a parametrized test at each
edge and edge ± 0.05 (e.g. 70 → "Mogelijk", 200 → "Substantieel").

### P3 — PDF branches (`pdf.py`, 91%)
Only the "one hazard, no residual" path runs. Cover the empty-assessment
branch (lines 101-105) and a hazard with full residual values (residual
coloring path).

### P4 — Model properties (`models/rie.py`)
`Hazard.risk_action` and `has_residual` are never asserted directly, and
`residual_risk_score` is only seen through the API. Add model unit tests,
including a partial-residual set at the model level (bypassing the schema
validator) to pin `residual_risk_score is None`.

### P5 — Schema validation edges
Untested: per-field residual scale validators (e.g. `residual_probability=7`
→ 422), `description` min/max length, `category`/`control_measure` max length,
incident field lengths and `occurred_on` parsing.

### P6 — CRUD semantics
Untested intent: `list_assessments` "newest first" ordering,
`list_incidents` ordering (`occurred_on desc, id desc`), and
`delete_assessment` cascade-deleting its hazards.

### P7 — Remaining API/web gaps
`GET /api/assessments` (list), `DELETE /api/assessments/{id}` (+404),
incident API `GET`/`DELETE` 404s, the `ValueError → 422` branch in
`api.add_hazard`, `/health`, and the incident web detail/edit/delete forms.

## Tooling recommendation
`pytest-cov` is not currently a dependency. Add it to `requirements.txt`
and enforce a floor in `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --cov=app --cov-report=term-missing --cov-fail-under=88
```

This turns the gaps above into a tracked, regression-proof number. Raising
the web layer to parity would push total coverage well into the mid-90s.
