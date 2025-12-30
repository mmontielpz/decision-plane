import json
from pathlib import Path
from app.training.evaluation_report import write_evaluation_report


def test_write_evaluation_report(tmp_path):
    output = tmp_path / "eval.json"

    metrics = {
        "precision": 0.8,
        "recall": 0.6,
        "f1": 0.685,
    }

    write_evaluation_report(
        metrics=metrics,
        dataset_path=Path("data/dataset.jsonl"),
        model_path=Path("models/baseline.joblib"),
        feature_version="v1",
        label_version=1,
        output_path=output,
        notes="Baseline logistic regression",
    )

    assert output.exists()

    content = json.loads(output.read_text())
    assert content["metrics"]["precision"] == 0.8
    assert content["feature_version"] == "v1"
    assert content["label_version"] == 1
