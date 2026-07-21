# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

SHE-Programs is a collection of Safety, Health and Environment tools from AMM Consultancy. It currently contains one program:

- **`rie_toetsing/`** — the RI&E-toets-tool: a Python CLI (`rie-toets`) that tests a Dutch Risico-Inventarisatie & -Evaluatie (RI&E) and Plan van Aanpak against the legal review criteria (Staatscourant 2024 nr. 39674) using the Claude API, and generates a "Toets- en adviesrapport" as Markdown or Word.

**The entire codebase is in Dutch** — identifiers, docstrings, comments, CLI help text, and user-facing output. Keep new code and documentation in Dutch and follow the existing naming style (e.g. `laad_document`, `toetser`, `oordeel`, `bevinding`, `advies`).

## Commands

All commands run from the `rie_toetsing/` directory:

```bash
# Setup (Python >= 3.11)
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env        # requires ANTHROPIC_API_KEY for real toetsing runs

# Tests (offline, no API key needed)
pip install pytest
pytest                                        # all tests (testpaths = tests/)
pytest tests/test_rapport.py                  # one file
pytest tests/test_rapport.py::test_naam       # one test

# Run the CLI without an API call (empty report template)
rie-toets some.pdf --dry-run -o sjabloon.docx

# Full run (needs ANTHROPIC_API_KEY)
rie-toets RIE.pdf --pva PvA.pdf --org "Voorbeeld B.V." -o toetsrapport.docx

# Regenerate HANDLEIDING.docx after editing HANDLEIDING.md
python tools/markdown_naar_docx.py HANDLEIDING.md HANDLEIDING.docx
```

There is no linter or formatter configured.

## Architecture

The tool is a linear pipeline, one module per stage (`rie_toetsing/rie_toetsing/`):

1. **`documenten.py`** — reads source documents into frozen `Document` dataclasses. PDFs are base64-encoded and sent to the Claude API as `document` content blocks (never parsed locally); `.docx`/`.txt`/`.md` become plain-text blocks. `naar_contentblokken()` produces the API message content.
2. **`criteria.py`** — the single source of truth for all toetsregels (1.1.1–1.4.4 for the RI&E, 2.1–2.10 for the Plan van Aanpak) as `Criterium` dataclasses, grouped per report table (`VOLLEDIGHEID`, `BETROUWBAARHEID`, `ACTUALITEIT`, `ACTUELE_INZICHTEN`, `PLAN_VAN_AANPAK`). Some criteria are merged into combined IDs (e.g. `"1.1.5 / 1.1.8 / 1.1.9"`) exactly as prescribed by the AMM template v2.2 — do not split them. Also defines the allowed oordelen (`Ja / Deels / Nee / n.v.t.`) and their RAG colors.
3. **`prompt.py`** — builds `SYSTEEMPROMPT` (the AKD persona plus criteria list, rendered from `criteria.py`) and `UITVOER_SCHEMA`, the JSON schema that constrains the model's structured output. Also holds `AKD_GEGEVENS` (the certified expert's fixed contact/registration details used in the report).
4. **`toetser.py`** — the only module that calls the Claude API. `toets()` streams a request with structured output (`output_config` with `json_schema`) and returns the parsed dict; `onderzoek_branche()` optionally gathers branch context via the web search tool first. Default model is `STANDAARD_MODEL` here.
5. **`rapport.py`** / **`rapport_docx.py`** — render the structured result into the report: Markdown, or Word in the AMM huisstijl (blue `#5467B0`, Aptos font, portrait cover/summary + landscape criteria tables, RAG-colored oordeel cells). `render_docx()` accepts an optional `--sjabloon` .docx whose margins/header/footer/logo are preserved.
6. **`cli.py`** — argument parsing and orchestration. Output format is derived from the `--output` extension or `--format`. After a run it warns about any criterium ID missing from the results.

The anthropic SDK and python-docx are **lazy-imported** inside the functions that need them, so `--dry-run`, Markdown rendering, and the tests work without those dependencies or an API key. Preserve this property when refactoring.

Data flows between stages as a plain dict matching `UITVOER_SCHEMA`; criterion IDs are the join key between the model's `toetsingen` list and the tables in `criteria.py`. When adding or changing a criterium, `prompt.py`, both report renderers, and the tests pick it up automatically via `criteria.py` — that is the only place to edit toetsregels.

## Conventions

- Terminology: always **"Kinney & Wiruth"**, never "Fine-Kinney".
- Report structure, merged criterium IDs, oordelen, and huisstijl follow the fixed AMM template v2.2; don't deviate without instruction.
- Tests must stay offline (no API key, no network) — they cover `criteria.py` and both report renderers.
- `HANDLEIDING.md` is the user manual for non-programmers; `HANDLEIDING.docx` is generated from it with `tools/markdown_naar_docx.py`, so regenerate the .docx whenever the .md changes.
- `Toets-RIE.bat` (guided) and `start.bat` (shell) are Windows entry points that self-install a `.venv`; `.gitattributes` forces CRLF line endings on `*.bat` — keep any new batch files consistent with that.
