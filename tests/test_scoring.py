"""Tests voor het Fine & Kinney-scoremodel."""

import pytest

from app.scoring import calculate_risk_score, classify_risk


def test_risk_score_multiplies_factors():
    # 6 (waarschijnlijk) x 6 (regelmatig) x 15 (ernstig) = 540
    assert calculate_risk_score(6, 6, 15) == 540


def test_lowest_score():
    assert calculate_risk_score(0.1, 0.5, 1) == pytest.approx(0.05)


@pytest.mark.parametrize("factor", ["probability", "exposure", "effect"])
def test_invalid_factor_raises(factor):
    args = {"probability": 6, "exposure": 6, "effect": 15}
    args[factor] = 999  # buiten de toegestane schaal
    with pytest.raises(ValueError):
        calculate_risk_score(**args)


@pytest.mark.parametrize(
    "score,expected",
    [
        (0, "Gering"),
        (10, "Gering"),
        (50, "Mogelijk"),
        (150, "Substantieel"),
        (300, "Hoog"),
        (540, "Zeer hoog"),
    ],
)
def test_classification(score, expected):
    assert classify_risk(score).label == expected
