from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import AuditLog, Company
from app.schemas.company import CompanyCreate, CompanyRead

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyRead])
def list_companies(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return list(db.scalars(select(Company).order_by(Company.id.desc()).limit(limit).offset(offset)))


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("", response_model=CompanyRead, status_code=201)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Company).where(Company.domain == payload.domain))
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Company with domain '{payload.domain}' already exists (id={existing.id})",
        )
    company = Company(**payload.model_dump())
    db.add(company)
    try:
        db.flush()
        db.add(
            AuditLog(
                actor_type="system",
                action="company.created",
                entity_type="company",
                entity_id=company.id,
                details={"domain": company.domain},
            )
        )
        db.commit()
    except IntegrityError:
        # Two requests created the same domain at the same time.
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Company with domain '{payload.domain}' already exists")
    return company
