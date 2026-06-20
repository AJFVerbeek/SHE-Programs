"""Opdrachtregel-interface voor de RI&E-toets-tool.

Voorbeeld:

    rie-toets RIE.pdf --pva PlanVanAanpak.pdf --org "Voorbeeld B.V." \\
        --output toetsrapport.md

Of zonder API-aanroep, voor een leeg sjabloon:

    rie-toets RIE.pdf --dry-run --output sjabloon.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .criteria import criterium_ids
from .documenten import laad_document
from .rapport import render


def _bouw_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rie-toets",
        description="Toets een RI&E en Plan van Aanpak aan de wettelijke "
        "toetsingscriteria (Stcrt. 2024 nr. 39674) en genereer een "
        "Toets- en adviesrapport (AMM Consultancy).",
    )
    parser.add_argument("rie", nargs="+", help="Pad(en) naar de RI&E-document(en).")
    parser.add_argument("--pva", action="append", default=[], metavar="PAD",
                        help="Plan van Aanpak (herhaalbaar).")
    parser.add_argument("--bhv", action="append", default=[], metavar="PAD",
                        help="BHV-plan (herhaalbaar).")
    parser.add_argument("--arbobeleid", action="append", default=[], metavar="PAD",
                        help="Arbobeleid (herhaalbaar).")
    parser.add_argument("--verdiepend", action="append", default=[], metavar="PAD",
                        help="Verdiepend onderzoek, bijv. PSA/MTO (herhaalbaar).")
    parser.add_argument("--org", default="", help="Naam van de organisatie.")
    parser.add_argument("--branche", default="", help="Branche of SBI-code (optioneel).")
    parser.add_argument("--branche-onderzoek", action="store_true",
                        help="Verzamel vooraf branche-context via web search.")
    parser.add_argument("--model", default=None, help="Te gebruiken Claude-model.")
    parser.add_argument("--output", "-o", default=None, metavar="PAD",
                        help="Schrijf het rapport naar dit bestand (anders stdout).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Lees alleen de documenten in en genereer een leeg sjabloon "
                        "(geen API-aanroep).")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _laad_alles(args: argparse.Namespace) -> list:
    documenten = []
    for pad in args.rie:
        documenten.append(laad_document(pad, "RI&E"))
    for pad in args.pva:
        documenten.append(laad_document(pad, "Plan van Aanpak"))
    for pad in args.bhv:
        documenten.append(laad_document(pad, "BHV-plan"))
    for pad in args.arbobeleid:
        documenten.append(laad_document(pad, "Arbobeleid"))
    for pad in args.verdiepend:
        documenten.append(laad_document(pad, "Verdiepend onderzoek"))
    return documenten


def _schrijf(rapport: str, output: str | None) -> None:
    if output:
        Path(output).write_text(rapport, encoding="utf-8")
        print(f"Rapport geschreven naar: {output}", file=sys.stderr)
    else:
        print(rapport)


def main(argv: list[str] | None = None) -> int:
    args = _bouw_parser().parse_args(argv)

    try:
        documenten = _laad_alles(args)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Fout bij inlezen: {exc}", file=sys.stderr)
        return 1

    bestandsnamen = ", ".join(f"{d.label}: {d.bestandsnaam}" for d in documenten)
    print(f"Ingelezen documenten: {bestandsnamen}", file=sys.stderr)

    if args.dry_run:
        print("Dry run: leeg sjabloon zonder API-aanroep.", file=sys.stderr)
        data = {"organisatieprofiel": {"organisatienaam": args.org}}
        _schrijf(render(data), args.output)
        return 0

    # Lazy import: de SDK is alleen nodig voor een echte toetsing.
    from .toetser import STANDAARD_MODEL, onderzoek_branche, toets

    model = args.model or STANDAARD_MODEL
    branche_context = ""
    try:
        if args.branche_onderzoek and args.org:
            print("Branche-onderzoek via web search…", file=sys.stderr)
            branche_context = onderzoek_branche(args.org, args.branche, model=model)

        print(f"Toetsen met model {model}…", file=sys.stderr)
        data = toets(
            documenten,
            organisatie=args.org,
            branche_context=branche_context,
            model=model,
        )
    except RuntimeError as exc:
        print(f"Fout tijdens toetsing: {exc}", file=sys.stderr)
        return 1

    # Controleer of alle toetsregels beoordeeld zijn.
    beoordeeld = {t.get("id") for t in data.get("toetsingen", [])}
    ontbreekt = [cid for cid in criterium_ids() if cid not in beoordeeld]
    if ontbreekt:
        print(
            "Let op: geen oordeel voor toetsregel(s): " + ", ".join(ontbreekt),
            file=sys.stderr,
        )

    _schrijf(render(data), args.output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
