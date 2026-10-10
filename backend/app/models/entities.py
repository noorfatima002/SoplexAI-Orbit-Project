"""All Orbit V1 tables. Statuses are plain strings guarded by CHECK constraints (portable, easy to extend)."""
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    false,
    func,
    text,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

USER_ROLES = ("admin", "member")
ACTOR_TYPES = ("user", "agent", "system")
LEAD_STATUSES = ("new", "researched", "qualified", "disqualified", "contacted", "replied", "won", "lost")
CHANNELS = ("email", "linkedin", "upwork")
OUTREACH_STATUSES = ("draft", "pending_approval", "approved", "rejected", "sent", "failed")
FOLLOWUP_STATUSES = ("pending", "done", "skipped", "cancelled")
RESPONSE_INTENTS = ("interested", "not_interested", "question", "out_of_office", "unsubscribe", "other")
JOB_STATUSES = ("queued", "running", "succeeded", "failed", "retrying")


def _in(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint(_in("role", USER_ROLES), name="role_valid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="member", server_default="member", nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=true(), nullable=False)


class Company(TimestampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Normalized domain (e.g. "acme.com") is the de-duplication key.
    domain: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    website: Mapped[str | None] = mapped_column(String(500))
    industry: Mapped[str | None] = mapped_column(String(100))
    size_range: Mapped[str | None] = mapped_column(String(50))
    country: Mapped[str | None] = mapped_column(String(2))
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(100))
    source_url: Mapped[str | None] = mapped_column(String(500))

    contacts: Mapped[list["Contact"]] = relationship(
        back_populates="company", cascade="all, delete-orphan", passive_deletes=True
    )


class Contact(TimestampMixin, Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint("company_id", "email", name="uq_contacts_company_id_email"),
        Index("ix_contacts_company_id", "company_id"),
        Index("ix_contacts_email", "email"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    job_title: Mapped[str | None] = mapped_column(String(100))
    linkedin_url: Mapped[str | None] = mapped_column(String(500))
    phone: Mapped[str | None] = mapped_column(String(50))
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false(), nullable=False)

    company: Mapped[Company] = relationship(back_populates="contacts")


class Lead(TimestampMixin, Base):
    __tablename__ = "leads"
    __table_args__ = (
        CheckConstraint(_in("status", LEAD_STATUSES), name="status_valid"),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="score_range"),
        Index("ix_leads_status", "status"),
        Index("ix_leads_score", "score"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # One lead per company in V1.
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), default="new", server_default="new", nullable=False)
    score: Mapped[int | None] = mapped_column(Integer)
    score_reason: Mapped[str | None] = mapped_column(Text)
    ai_signals: Mapped[Any | None] = mapped_column(JSON)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    company: Mapped[Company] = relationship()


class ResearchNote(Base):
    __tablename__ = "research_notes"
    __table_args__ = (Index("ix_research_notes_company_id", "company_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    signals: Mapped[Any | None] = mapped_column(JSON)
    source_url: Mapped[str | None] = mapped_column(String(500))
    model_name: Mapped[str | None] = mapped_column(String(100))
    created_by: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OutreachMessage(TimestampMixin, Base):
    __tablename__ = "outreach_messages"
    __table_args__ = (
        CheckConstraint(_in("channel", CHANNELS), name="channel_valid"),
        CheckConstraint(_in("status", OUTREACH_STATUSES), name="status_valid"),
        # Human approval rule: nothing can be approved or sent without a named approver.
        CheckConstraint("status NOT IN ('approved', 'sent') OR approved_by IS NOT NULL", name="approval_required"),
        Index("ix_outreach_messages_lead_id", "lead_id"),
        Index("ix_outreach_messages_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    contact_id: Mapped[int | None] = mapped_column(ForeignKey("contacts.id", ondelete="SET NULL"))
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="draft", server_default="draft", nullable=False)
    # RESTRICT: a user who approved messages cannot be deleted (keeps the audit trail intact).
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)


class FollowUp(TimestampMixin, Base):
    __tablename__ = "follow_ups"
    __table_args__ = (
        CheckConstraint(_in("status", FOLLOWUP_STATUSES), name="status_valid"),
        Index("ix_follow_ups_due_status", "due_at", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    outreach_message_id: Mapped[int | None] = mapped_column(ForeignKey("outreach_messages.id", ondelete="SET NULL"))
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", server_default="pending", nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, server_default=text("1"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (
        CheckConstraint(_in("channel", CHANNELS), name="channel_valid"),
        CheckConstraint(f"intent IS NULL OR {_in('intent', RESPONSE_INTENTS)}", name="intent_valid"),
        Index("ix_responses_lead_id", "lead_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    outreach_message_id: Mapped[int | None] = mapped_column(ForeignKey("outreach_messages.id", ondelete="SET NULL"))
    channel: Mapped[str] = mapped_column(String(20), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    intent: Mapped[str | None] = mapped_column(String(30))
    confidence: Mapped[float | None] = mapped_column(Float)
    recommended_action: Mapped[str | None] = mapped_column(Text)
    handled: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OptOut(Base):
    """Do-not-contact list. Agents MUST check this before preparing or sending anything."""

    __tablename__ = "opt_outs"
    __table_args__ = (CheckConstraint("email IS NOT NULL OR domain IS NOT NULL", name="email_or_domain"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    domain: Mapped[str | None] = mapped_column(String(255), unique=True)
    reason: Mapped[str | None] = mapped_column(String(255))
    source: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        CheckConstraint(_in("actor_type", ACTOR_TYPES), name="actor_type_valid"),
        Index("ix_audit_log_entity", "entity_type", "entity_id"),
        Index("ix_audit_log_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    actor_type: Mapped[str] = mapped_column(String(20), default="system", server_default="system", nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(50))
    entity_id: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[Any | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class JobRun(TimestampMixin, Base):
    """Tracks every agent/workflow run: status, retries, errors. idempotency_key prevents duplicate runs."""

    __tablename__ = "job_runs"
    __table_args__ = (
        CheckConstraint(_in("status", JOB_STATUSES), name="status_valid"),
        Index("ix_job_runs_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="queued", server_default="queued", nullable=False)
    attempt: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"), nullable=False)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3, server_default=text("3"), nullable=False)
    input_payload: Mapped[Any | None] = mapped_column(JSON)
    result: Mapped[Any | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), unique=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
