from app.serving.review_queue_repository import get_review_queue


class ReviewQueueAdapter:
    """
    Product-facing adapter for the Review Queue (v1).

    Responsibilities:
    - Delegate data access to the read-model repository
    - Expose a stable, UI-oriented DTO
    - Contain NO SQL and NO business logic
    """

    def list_review_queue(self) -> list[dict]:
        """
        Returns the list of documents requiring human review.

        The shape and semantics are defined by the review queue contract (v1).
        """
        return get_review_queue()
