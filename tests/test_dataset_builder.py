import json
from pathlib import Path
from app.training.dataset_builder import build_training_dataset
from app.labels.repository import insert_label


def test_build_training_dataset(tmp_path):
    # Prepare fake features file
    features_file = tmp_path / "features.jsonl"
    output_file = tmp_path / "dataset.jsonl"

    features = [
        {"document_id": "doc_001", "f1": 1.0},
        {"document_id": "doc_002", "f1": 0.5},
    ]

    with features_file.open("w", encoding="utf-8") as f:
        for rec in features:
            f.write(json.dumps(rec) + "\n")

    # Insert one label
    insert_label(
        document_id="doc_001",
        label_value="high",
        label_type="risk_level",
        label_source="manual_review",
        label_timestamp="2025-01-10T10:00:00",
        label_version=1,
        confidence=0.9,
    )

    # Build dataset
    written = build_training_dataset(
        features_path=features_file,
        output_path=output_file,
    )

    assert written == 2
    assert output_file.exists()

    rows = [json.loads(line) for line in output_file.read_text().splitlines()]

    # doc_001 has label
    assert len(rows[0]["labels"]) == 1
    assert rows[0]["labels"][0]["label_value"] == "high"

    # doc_002 has no labels
    assert rows[1]["labels"] == []
