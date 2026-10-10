"""initial schema: 11 tables for Orbit V1

Revision ID: 0001
Revises:
Create Date: 2026-10-10
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    ]


def _created_at() -> sa.Column:
    return sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=20), server_default="member", nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        *_timestamps(),
        sa.CheckConstraint("role IN ('admin', 'member')", name=op.f("ck_users_role_valid")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("size_range", sa.String(length=50), nullable=True),
        sa.Column("country", sa.String(length=2), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_companies")),
        sa.UniqueConstraint("domain", name=op.f("uq_companies_domain")),
    )

    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("job_title", sa.String(length=100), nullable=True),
        sa.Column("linkedin_url", sa.String(length=500), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("email_verified", sa.Boolean(), server_default=sa.false(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name=op.f("fk_contacts_company_id_companies"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contacts")),
        sa.UniqueConstraint("company_id", "email", name="uq_contacts_company_id_email"),
    )
    op.create_index("ix_contacts_company_id", "contacts", ["company_id"])
    op.create_index("ix_contacts_email", "contacts", ["email"])

    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="new", nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("score_reason", sa.Text(), nullable=True),
        sa.Column("ai_signals", sa.JSON(), nullable=True),
        sa.Column("assigned_to", sa.Integer(), nullable=True),
        *_timestamps(),
        sa.CheckConstraint(
            "status IN ('new', 'researched', 'qualified', 'disqualified', 'contacted', 'replied', 'won', 'lost')",
            name=op.f("ck_leads_status_valid"),
        ),
        sa.CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name=op.f("ck_leads_score_range")),
        sa.ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name=op.f("fk_leads_company_id_companies"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["assigned_to"], ["users.id"], name=op.f("fk_leads_assigned_to_users"), ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
        sa.UniqueConstraint("company_id", name=op.f("uq_leads_company_id")),
    )
    op.create_index("ix_leads_status", "leads", ["status"])
    op.create_index("ix_leads_score", "leads", ["score"])

    op.create_table(
        "research_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("signals", sa.JSON(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        sa.Column("created_by", sa.String(length=50), nullable=True),
        _created_at(),
        sa.ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name=op.f("fk_research_notes_company_id_companies"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"], ["leads.id"], name=op.f("fk_research_notes_lead_id_leads"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_research_notes")),
    )
    op.create_index("ix_research_notes_company_id", "research_notes", ["company_id"])

    op.create_table(
        "outreach_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="draft", nullable=False),
        sa.Column("approved_by", sa.Integer(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        *_timestamps(),
        sa.CheckConstraint("channel IN ('email', 'linkedin', 'upwork')", name=op.f("ck_outreach_messages_channel_valid")),
        sa.CheckConstraint(
            "status IN ('draft', 'pending_approval', 'approved', 'rejected', 'sent', 'failed')",
            name=op.f("ck_outreach_messages_status_valid"),
        ),
        sa.CheckConstraint(
            "status NOT IN ('approved', 'sent') OR approved_by IS NOT NULL",
            name=op.f("ck_outreach_messages_approval_required"),
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"], ["leads.id"], name=op.f("fk_outreach_messages_lead_id_leads"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"], ["contacts.id"], name=op.f("fk_outreach_messages_contact_id_contacts"), ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["approved_by"], ["users.id"], name=op.f("fk_outreach_messages_approved_by_users"), ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_outreach_messages")),
    )
    op.create_index("ix_outreach_messages_lead_id", "outreach_messages", ["lead_id"])
    op.create_index("ix_outreach_messages_status", "outreach_messages", ["status"])

    op.create_table(
        "follow_ups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("outreach_message_id", sa.Integer(), nullable=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("attempt_number", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.CheckConstraint(
            "status IN ('pending', 'done', 'skipped', 'cancelled')", name=op.f("ck_follow_ups_status_valid")
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"], ["leads.id"], name=op.f("fk_follow_ups_lead_id_leads"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["outreach_message_id"],
            ["outreach_messages.id"],
            name=op.f("fk_follow_ups_outreach_message_id_outreach_messages"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_follow_ups")),
    )
    op.create_index("ix_follow_ups_due_status", "follow_ups", ["due_at", "status"])

    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("outreach_message_id", sa.Integer(), nullable=True),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("intent", sa.String(length=30), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("recommended_action", sa.Text(), nullable=True),
        sa.Column("handled", sa.Boolean(), server_default=sa.false(), nullable=False),
        _created_at(),
        sa.CheckConstraint("channel IN ('email', 'linkedin', 'upwork')", name=op.f("ck_responses_channel_valid")),
        sa.CheckConstraint(
            "intent IS NULL OR intent IN ('interested', 'not_interested', 'question', 'out_of_office', 'unsubscribe', 'other')",
            name=op.f("ck_responses_intent_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"], ["leads.id"], name=op.f("fk_responses_lead_id_leads"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["outreach_message_id"],
            ["outreach_messages.id"],
            name=op.f("fk_responses_outreach_message_id_outreach_messages"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_responses")),
    )
    op.create_index("ix_responses_lead_id", "responses", ["lead_id"])

    op.create_table(
        "opt_outs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        _created_at(),
        sa.CheckConstraint("email IS NOT NULL OR domain IS NOT NULL", name=op.f("ck_opt_outs_email_or_domain")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_opt_outs")),
        sa.UniqueConstraint("email", name=op.f("uq_opt_outs_email")),
        sa.UniqueConstraint("domain", name=op.f("uq_opt_outs_domain")),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("actor_type", sa.String(length=20), server_default="system", nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        _created_at(),
        sa.CheckConstraint("actor_type IN ('user', 'agent', 'system')", name=op.f("ck_audit_log_actor_type_valid")),
        sa.ForeignKeyConstraint(
            ["actor_user_id"], ["users.id"], name=op.f("fk_audit_log_actor_user_id_users"), ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_log")),
    )
    op.create_index("ix_audit_log_entity", "audit_log", ["entity_type", "entity_id"])
    op.create_index("ix_audit_log_created_at", "audit_log", ["created_at"])

    op.create_table(
        "job_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="queued", nullable=False),
        sa.Column("attempt", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("max_attempts", sa.Integer(), server_default=sa.text("3"), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=True),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=100), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.CheckConstraint(
            "status IN ('queued', 'running', 'succeeded', 'failed', 'retrying')",
            name=op.f("ck_job_runs_status_valid"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_job_runs")),
        sa.UniqueConstraint("idempotency_key", name=op.f("uq_job_runs_idempotency_key")),
    )
    op.create_index("ix_job_runs_status", "job_runs", ["status"])


def downgrade() -> None:
    for table in (
        "job_runs",
        "audit_log",
        "opt_outs",
        "responses",
        "follow_ups",
        "outreach_messages",
        "research_notes",
        "leads",
        "contacts",
        "companies",
        "users",
    ):
        op.drop_table(table)
