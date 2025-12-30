from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split


def load_dataset(dataset_path: Path):
    X = []
    y = []

    with dataset_path.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)

            # Simple numeric features only (MVP)
            features = {k: v for k, v in rec.items() if k.startswith("f")}
            X.append(list(features.values()))

            # Binary target from labels
            labels = rec.get("labels", [])
            target = 0
            for lbl in labels:
                if lbl["label_type"] == "risk_level" and lbl["label_value"] == "high":
                    target = 1
                    break
            y.append(target)

    return np.array(X), np.array(y)


def train_and_evaluate(
    *,
    dataset_path: Path,
    model_path: Path,
    report_path: Path,
):
    X, y = load_dataset(dataset_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="binary", zero_division=0
    )

    report = {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "num_train": int(len(y_train)),
        "num_test": int(len(y_test)),
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    report_path.write_text(json.dumps(report, indent=2))

    return report
