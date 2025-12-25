# tests/test_feedback_repository.py

from app.feedback.repository import FeedbackRepository


def test_insert_feedback_is_idempotent(clean_state):
    repo = FeedbackRepository()

    fid1 = repo.insert_feedback_event(
        external_id="fb-123",
        source="human-review",
        feedback_value="POSITIVE",
        confidence=0.9,
    )

    fid2 = repo.insert_feedback_event(
        external_id="fb-123",
        source="human-review",
        feedback_value="POSITIVE",
        confidence=0.9,
    )

    assert fid1 == fid2


def test_link_feedback_to_prediction(clean_state):
    repo = FeedbackRepository()

    feedback_id = repo.insert_feedback_event(
        external_id="fb-456",
        source="audit",
        feedback_value="NEGATIVE",
    )

    # Fake prediction_event_id for linkage test
    repo.link_feedback_to_prediction(
        feedback_id=feedback_id,
        prediction_event_id=1,
    )

    # No exception == linkage accepted (idempotent insert)
