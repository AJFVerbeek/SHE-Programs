"""Tests voor de toetsingscriteria."""

from rie_toetsing import criteria
from rie_toetsing.prompt import UITVOER_SCHEMA


def test_aantal_criteria():
    # 13 volledigheid + 2 actualiteit + 2 actuele inzichten + 2 betrouwbaarheid
    assert len(criteria.RIE_CRITERIA) == 19
    # + 10 Plan van Aanpak
    assert len(criteria.PLAN_VAN_AANPAK) == 10
    assert len(criteria.ALLE_CRITERIA) == 29


def test_unieke_ids():
    ids = criteria.criterium_ids()
    assert len(ids) == len(set(ids)), "criterium-id's moeten uniek zijn"


def test_samenvoegingen_aanwezig():
    ids = set(criteria.criterium_ids())
    assert "1.1.5 / 1.1.8 / 1.1.9" in ids
    assert "1.1.6 / 1.1.10" in ids
    assert "1.1.13 / 1.1.14" in ids
    assert "1.4.1 / 1.4.2 / 1.4.3" in ids


def test_oordelen_en_rag():
    assert criteria.OORDELEN == ("Ja", "Deels", "Nee", "n.v.t.")
    for oordeel in criteria.OORDELEN:
        assert oordeel in criteria.RAG_KLEUR


def test_schema_oordeel_enum_komt_overeen():
    enum = UITVOER_SCHEMA["properties"]["toetsingen"]["items"]["properties"]["oordeel"][
        "enum"
    ]
    assert enum == list(criteria.OORDELEN)
