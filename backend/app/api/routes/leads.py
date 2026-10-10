from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Lead
from app.schemas.lead import LeadRead

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=list[LeadRead])
def list_leads(
    status: str | None = None,
    min_score: int | None = Query(None, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Lead)
    if status:
        stmt = stmt.where(Lead.status == status)
    if min_score is not None:
        stmt = stmt.where(Lead.score >= min_score)
    stmt = stmt.order_by(Lead.score.desc().nulls_last(), Lead.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt))
