from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import JobRun
from app.schemas.job import AgentRunRequest, JobRunRead

router = APIRouter(prefix="/agents", tags=["agents"])

# Only the Lead Generation Agent is planned for the first milestone.
ENABLED_AGENTS = {"lead_generation"}


@router.post("/run", response_model=JobRunRead, status_code=202)
def run_agent(payload: AgentRunRequest, db: Session = Depends(get_db)):
    """Queue an agent run. Phase 1: records the job only; the agent worker comes in Phase 2."""
    if payload.agent not in ENABLED_AGENTS:
        raise HTTPException(status_code=501, detail=f"Agent '{payload.agent}' is not available in V1 yet")

    key = payload.idempotency_key
    if key:
        existing = db.scalar(select(JobRun).where(JobRun.idempotency_key == key))
        if existing is not None:
            return existing

    job = JobRun(
        job_type=payload.agent,
        status="queued",
        input_payload=payload.params,
        idempotency_key=key,
    )
    db.add(job)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.scalar(select(JobRun).where(JobRun.idempotency_key == key))
        if existing is None:
            raise
        return existing
    db.refresh(job)
    return job


@router.get("/jobs/{job_id}", response_model=JobRunRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(JobRun, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
