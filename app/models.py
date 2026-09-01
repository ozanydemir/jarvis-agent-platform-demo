from enum import StrEnum

from pydantic import BaseModel, Field


class Decision(StrEnum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


class AssistantRequest(BaseModel):
    message: str = Field(min_length=3, max_length=500)


class TraceStep(BaseModel):
    stage: str
    status: str
    detail: str
    elapsed_ms: int = Field(ge=0)


class AssistantResult(BaseModel):
    intent: str
    adapter: str
    decision: Decision
    response: str
    requires_human: bool
    trace: list[TraceStep]
