import json
from pathlib import Path
from app.training.train_baseline import train_and_evaluate


def test_train_baseline(tmp_path):
    dataset = tmp_path / "dataset.jsonl"
    model_path = tmp_path / "model.joblib"
    report_path = tmp_path / "report.json"

    records = [
        {"document_id": "doc_1", "f1": 1.0, "labels": [{"label_type": "risk_level", "label_value": "high"}]},
        {"document_id": "doc_2", "f1": 0.2, "labels": []},
        {"document_id": "doc_3", "f1": 0.8, "labels": [{"label_type": "risk_level", "label_value": "high"}]},
        {"document_id": "doc_4", "f1": 0.1, "labels": []},
    ]

    with dataset.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    report = train_and_evaluate(
        dataset_path=dataset,
        model_path=model_path,
        report_path=report_path,
    )

    assert model_path.exists()
    assert report_path.exists()
    assert "precision" in report
    assert "recall" in report
