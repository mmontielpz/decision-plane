from pydantic import BaseModel, ConfigDict


class ReplayDecisionV1(BaseModel):
    document_id: str
    score: float

    old_threshold: float
    old_decision: str

    new_threshold: float
    new_decision: str

    changed: bool

    model_config = ConfigDict(
        extra="forbid"
    )
