from pathlib import Path
import json
from typing import Dict
from app.db.database import get_connection


def load_labels_map() -> Dict[str, list[dict]]:
    """
    Load labels from SQLite and group by document_id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            document_id,
            label_value,
            label_type,
            label_source,
            label_timestamp,
            label_version,
            confidence
        FROM labels
        """
    )

    rows = cursor.fetchall()
    conn.close()

    labels_by_doc: Dict[str, list[dict]] = {}

    for (
        document_id,
        label_value,
        label_type,
        label_source,
        label_timestamp,
        label_version,
        confidence,
    ) in rows:
        labels_by_doc.setdefault(document_id, []).append(
            {
                "label_value": label_value,
                "label_type": label_type,
                "label_source": label_source,
                "label_timestamp": label_timestamp,
                "label_version": label_version,
                "confidence": confidence,
            }
        )

    return labels_by_doc


def build_training_dataset(
    *,
    features_path: Path,
    output_path: Path,
) -> int:
    """
    Build an offline training dataset by joining features with labels.

    Returns:
        Number of records written.
    """
    labels_by_doc = load_labels_map()

    records_written = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with features_path.open("r", encoding="utf-8") as f_in, output_path.open(
        "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            feature_record = json.loads(line)
            document_id = feature_record["document_id"]

            joined_record = {
                **feature_record,
                "labels": labels_by_doc.get(document_id, []),
            }

            f_out.write(json.dumps(joined_record) + "\n")
            records_written += 1

    return records_written
