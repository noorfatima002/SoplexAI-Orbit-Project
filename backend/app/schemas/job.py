from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

AgentName = Literal["lead_generation", "outreach", "follow_up", "response"]


class AgentRunRequest(BaseModel):
    agent: AgentName
    params: dict[str, Any] = Field(default_factory=dict)
    # Send the same key twice and you get the same job back instead of a duplicate run.
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=100)


class JobRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    status: str
    attempt: int
    max_attempts: int
    idempotency_key: str | None
    error_message: str | None
    created_at: datetime
