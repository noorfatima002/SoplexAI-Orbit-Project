import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Company, Contact, Lead, OptOut, OutreachMessage, User


def test_insert_company_and_contact(db_session):
    company = Company(name="Acme", domain="acme.com")
    company.contacts.append(Contact(full_name="Jane Doe", email="jane@acme.com"))
    db_session.add(company)
    db_session.commit()
    assert db_session.query(Contact).count() == 1


def test_company_domain_must_be_unique(db_session):
    db_session.add_all([Company(name="A", domain="acme.com"), Company(name="B", domain="acme.com")])
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_lead_score_must_be_0_to_100(db_session):
    company = Company(name="Acme", domain="acme.com")
    db_session.add(company)
    db_session.flush()
    db_session.add(Lead(company_id=company.id, score=150))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_message_cannot_be_approved_without_an_approver(db_session):
    company = Company(name="Acme", domain="acme.com")
    db_session.add(company)
    db_session.flush()
    lead = Lead(company_id=company.id)
    db_session.add(lead)
    db_session.flush()
    db_session.add(OutreachMessage(lead_id=lead.id, channel="email", body="Hi", status="approved"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_message_can_be_approved_with_an_approver(db_session):
    user = User(email="admin@soplexai.com", role="admin")
    company = Company(name="Acme", domain="acme.com")
    db_session.add_all([user, company])
    db_session.flush()
    lead = Lead(company_id=company.id)
    db_session.add(lead)
    db_session.flush()
    db_session.add(
        OutreachMessage(lead_id=lead.id, channel="email", body="Hi", status="approved", approved_by=user.id)
    )
    db_session.commit()


def test_opt_out_needs_email_or_domain(db_session):
    db_session.add(OptOut(reason="empty"))
    with pytest.raises(IntegrityError):
        db_session.commit()
