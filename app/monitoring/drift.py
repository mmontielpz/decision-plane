# app/monitoring/drift.py

from typing import Iterable, Dict, List
import math


def _safe_log(x: float) -> float:
    if x <= 0:
        return 0.0
    return math.log(x)


# -------------------------
# Prediction drift (PSI)
# -------------------------
def population_stability_index(
    reference: Iterable[float],
    current: Iterable[float],
    bins: int = 10,
) -> float:
    """
    Computes PSI between reference and current score distributions.

    PSI interpretation (rule of thumb):
        < 0.1   no drift
        0.1–0.2 moderate drift
        > 0.2   significant drift
    """
    ref = list(reference)
    cur = list(current)

    if not ref or not cur:
        return 0.0

    min_val = min(ref + cur)
    max_val = max(ref + cur)

    if min_val == max_val:
        return 0.0

    bin_width = (max_val - min_val) / bins

    def _hist(values: List[float]) -> List[float]:
        counts = [0] * bins
        for v in values:
            idx = int((v - min_val) / bin_width)
            if idx == bins:
                idx -= 1
            counts[idx] += 1
        total = len(values)
        return [c / total for c in counts]

    ref_dist = _hist(ref)
    cur_dist = _hist(cur)

    psi = 0.0
    for r, c in zip(ref_dist, cur_dist):
        if r == 0 and c == 0:
            continue
        psi += (c - r) * (_safe_log(c) - _safe_log(r))

    return psi


# -------------------------
# Decision drift (rate shift)
# -------------------------
def decision_rate_shift(
    reference_decisions: Iterable[str],
    current_decisions: Iterable[str],
    decision_value: str,
) -> float:
    """
    Computes absolute rate shift for a specific decision
    (e.g. REVIEW rate drift).
    """
    ref = list(reference_decisions)
    cur = list(current_decisions)

    if not ref or not cur:
        return 0.0

    ref_rate = ref.count(decision_value) / len(ref)
    cur_rate = cur.count(decision_value) / len(cur)

    return abs(cur_rate - ref_rate)


# -------------------------
# Threshold-based drift flag
# -------------------------
def drift_exceeds_threshold(
    metric_value: float,
    threshold: float,
) -> bool:
    """
    Explicit decision rule.
    No hidden heuristics.
    """
    return metric_value >= threshold
