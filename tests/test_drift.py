# tests/test_drift.py

from app.monitoring.drift import (
    population_stability_index,
    decision_rate_shift,
    drift_exceeds_threshold,
)


def test_psi_no_drift_identical_distributions():
    ref = [0.1, 0.2, 0.3, 0.4, 0.5]
    cur = [0.1, 0.2, 0.3, 0.4, 0.5]

    psi = population_stability_index(ref, cur)

    assert psi == 0.0


def test_psi_detects_distribution_shift():
    ref = [0.1] * 100 + [0.2] * 100
    cur = [0.8] * 100 + [0.9] * 100

    psi = population_stability_index(ref, cur)

    assert psi > 0.2


def test_psi_empty_input_is_safe():
    psi = population_stability_index([], [0.1, 0.2])
    assert psi == 0.0

    psi = population_stability_index([0.1, 0.2], [])
    assert psi == 0.0


def test_decision_rate_shift_no_change():
    ref = ["ACCEPT", "REVIEW", "ACCEPT", "REVIEW"]
    cur = ["ACCEPT", "REVIEW", "ACCEPT", "REVIEW"]

    shift = decision_rate_shift(ref, cur, decision_value="REVIEW")

    assert shift == 0.0


def test_decision_rate_shift_detects_change():
    ref = ["ACCEPT"] * 8 + ["REVIEW"] * 2
    cur = ["ACCEPT"] * 2 + ["REVIEW"] * 8

    shift = decision_rate_shift(ref, cur, decision_value="REVIEW")

    assert shift > 0.5


def test_drift_threshold_flag():
    assert drift_exceeds_threshold(0.25, threshold=0.2) is True
    assert drift_exceeds_threshold(0.1, threshold=0.2) is False
