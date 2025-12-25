from pathlib import Path
from datetime import datetime
import json
from typing import Dict, Any


def write_evaluation_report(
    *,
    metrics: Dict[str, float],
    dataset_path: Path,
    model_path: Path,
    feature_version: str,
    label_version: int,
    output_path: Path,
    notes: str | None = None,
) -> None:
    """
    Write a formal offline evaluation report.

    This function does not recompute metrics.
    It wraps existing results with provenance and metadata.
    """
    report: Dict[str, Any] = {
        "created_at": datetime.utcnow().isoformat(),
        "dataset_path": str(dataset_path),
        "model_path": str(model_path),
        "feature_version": feature_version,
        "label_version": label_version,
        "metrics": metrics,
        "notes": notes or "",
        "limitations": [
            "Offline evaluation only",
            "Labels may be noisy or delayed",
            "Simple baseline model without tuning",
            "Temporal split may not reflect future drift",
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))
