from app.labels.repository import insert_label


def test_insert_label_success():
    inserted = insert_label(
        document_id="doc_001",
        label_value="high",
        label_type="risk_level",
        label_source="manual_review",
        label_timestamp="2025-01-10T10:00:00",
        label_version=1,
        confidence=0.9,
    )

    assert inserted is True


def test_insert_label_duplicate():
    insert_label(
        document_id="doc_002",
        label_value="low",
        label_type="risk_level",
        label_source="rule_engine",
        label_timestamp="2025-01-10T10:00:00",
        label_version=1,
        confidence=None,
    )

    inserted = insert_label(
        document_id="doc_002",
        label_value="low",
        label_type="risk_level",
        label_source="rule_engine",
        label_timestamp="2025-01-10T10:00:00",
        label_version=1,
        confidence=None,
    )

    assert inserted is False
