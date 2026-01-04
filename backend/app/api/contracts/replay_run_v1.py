from pydantic import BaseModel


class ReplayDecisionV1(BaseModel):
    document_id: str
    score: float

    old_threshold: float
    old_decision: str

    new_threshold: float
    new_decision: str

    changed: bool

    class Config:
        extra = "forbid"
