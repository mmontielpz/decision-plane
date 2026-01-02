from __future__ import annotations

from typing import List

from app.core.models.document import (
    Document,
    Prediction,
    Signal,
    SignalType,
    TriageResult,
)


def evaluate(
    document: Document,
    prediction: Prediction | None,
    *,
    confidence_threshold: float = 0.6,
) -> TriageResult:
    signals: List[Signal] = []

    if prediction is None:
        signals.append(
            Signal(
                type=SignalType.MISSING_PREDICTION,
                severity=3,
                description="No prediction available for document",
            )
        )
    else:
        if prediction.label is None:
            signals.append(
                Signal(
                    type=SignalType.UNKNOWN,
                    severity=2,
                    description="Prediction label is missing",
                )
            )

        if (
            prediction.confidence is None
            or prediction.confidence < confidence_threshold
        ):
            signals.append(
                Signal(
                    type=SignalType.LOW_CONFIDENCE,
                    severity=1,
                    description="Prediction confidence below threshold",
                )
            )

    requires_human_review = len(signals) > 0

    return TriageResult(
        requires_human_review=requires_human_review,
        signals=signals,
    )
