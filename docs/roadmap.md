# Orbit Development Roadmap

Status: Proposed plan for team review

## Phase 1 — Understanding and Setup

Milestones:
- Review SoplexAI business, target market, and ICP.
- Draft Orbit V1 requirements and architecture.
- Prepare backend, database, configuration, and workflow setup.
- Document the data model, security considerations, and technology risks.
- Verify local startup and initial tests.

Owners:
- Noor Ul Huda: initial focus on business, ICP, prospect sources,
  and lead-data workflow requirements.
- Noor Fatima: initial focus on backend, database, security,
  environment setup, and API structure.
- Both members: review the full product and approve shared decisions.

Testing criteria:
- Services start using the documented procedure.
- Health endpoints work.
- Initial automated tests pass.
- Repository and documentation are available for review.

## Phase 2 — Lead Generation Prototype

Proposed milestones:
- Agree on approved prospect sources and ICP rules.
- Implement candidate discovery and research interfaces.
- Define qualification factors and evidence storage.
- Add duplicate detection and job status tracking.

Testing criteria:
- Validate representative sample records.
- Check source references and required fields.
- Test duplicates, invalid inputs, and source failures.
- Require human review of uncertain qualifications.

## Phase 3 — Outreach and Follow-up Prototype

Proposed milestones:
- Generate personalized outreach drafts.
- Add approval and suppression checks.
- Track outreach status and follow-up tasks.
- Prevent follow-ups after replies or opt-outs.

Testing criteria:
- No message is sent without required approval.
- Opt-outs are respected.
- Repeated requests do not create unintended duplicate actions.
- Failures are logged and recoverable.

## Phase 4 — Response Classification and Dashboard

Proposed milestones:
- Classify replies and identify intent.
- Recommend next actions with confidence indicators.
- Provide an internal view of prospects and job status.
- Add access control and audit visibility.

Testing criteria:
- Test representative response categories.
- Escalate uncertain cases to humans.
- Verify authorization and audit events.

## Phase 5 — Controlled Pilot and Scaling

Proposed milestones:
- Run a limited, reviewed pilot.
- Measure qualification quality, response handling, latency, and cost.
- Improve reliability and monitoring.
- Evaluate readiness for higher daily prospect volumes.

Testing criteria:
- Review quality and compliance before expanding volume.
- Load-test before accepting the future target of 250 prospects/day.
- Establish cost limits, recovery procedures, and operational ownership.

## Dependencies and Governance

Later phases depend on agreement about requirements, approved sources,
data retention, integrations, human approval, and budget.

Dates for Phases 2-5 are not committed. The team should estimate them
after Phase 1 review and prioritization.
