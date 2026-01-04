from typing import List
from pydantic import BaseModel


class DecisionOutcomeItemV1(BaseModel):
    window_start: str
    window_end: str

    model_version: str
    feature_version: str
    threshold: float

    n_total: int
    n_accept: int
    n_review: int

    class Config:
        extra = "forbid"


class DecisionOutcomesV1(BaseModel):
    outcomes: List[DecisionOutcomeItemV1]

    class Config:
        extra = "forbid"
