from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    status: str
    score: int | None
    score_reason: str | None
    created_at: datetime
