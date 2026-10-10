# Orbit V1 Product Requirements Document

Status: Draft for team review

## 1. Purpose

Orbit is an internal sales intelligence platform for managing prospect
research, qualification, outreach preparation, follow-ups, and response
classification through a shared database and orchestration layer.

Phase 1 establishes requirements and a reproducible development
environment. It does not require the complete production agent system.

## 2. Intended Users

Authorized SoplexAI team members who research prospects, review
qualification results, approve outreach, and monitor sales activity.

## 3. Proposed Components

- FastAPI: application API and business operations.
- PostgreSQL: shared company, lead, research, and activity data.
- n8n: proposed workflow scheduling and orchestration.
- Specialist agents: modular services for defined sales tasks.
- Web dashboard: future interface for authorized team members.

The initial repository does not yet constitute a complete production
implementation of every component.

## 4. Functional Requirements

### Lead Generation Agent

Input: target market, ICP criteria, approved sources, and search limits.

Output: candidate companies, evidence, qualification factors, score,
source references, and research status.

Requirements:
- Use permitted sources.
- Record evidence and timestamps.
- Identify likely duplicates.
- Flag uncertain results for human review.

### Outreach Agent

Input: an approved and qualified prospect, company research, and an
approved messaging policy.

Output: a personalized draft, supporting research, and a review status.

Requirement: prepare drafts for human approval before sending.

### Follow-up Agent

Input: approved outreach records, interaction history, replies,
and opt-out status.

Output: suggested follow-up tasks and their due dates.

Requirement: stop follow-ups when a reply, opt-out, or suppression
condition requires it.

### Response/Sales Agent

Input: received message content and relevant interaction history.

Output: intent category, summary, urgency, confidence, and recommended
next action.

Requirement: uncertain or sensitive cases must be escalated to a human.

## 5. Shared Data

The proposed model includes companies, contacts, leads, research records,
outreach drafts, follow-up activities, responses, jobs, and audit events.
See data_model.md for the initial schema proposal.

## 6. Human Approval

Human review is required before sending outreach, changing important
qualification rules, or taking actions that could materially affect a
prospect. Opt-outs and suppression rules must be enforced consistently.

## 7. Reliability

The design should provide:
- Input validation and useful error responses.
- Structured logs and job status tracking.
- Duplicate detection.
- Bounded retries for transient failures.
- Safe handling of repeated requests.
- A documented recovery process.
- Audit history for important changes.

## 8. Security and Privacy

Use environment variables for secrets, least-privilege access, appropriate
data retention, and access controls. Do not commit credentials. Collect
only necessary data and respect applicable laws and platform policies.

## 9. Out of Scope for Initial Phase

- Fully autonomous production outreach.
- A complete production dashboard.
- Voice and mobile access.
- Advanced vector search.
- A guaranteed capacity of 250 new prospects per day.

The 250-prospect target is a future scaling objective requiring
performance, quality, compliance, and cost testing.

## 10. Initial Acceptance Criteria

- Local services start using documented instructions.
- Health endpoints respond successfully.
- The database health check is verified.
- Initial API tests pass.
- Schema and architecture proposals are documented.
- Secrets remain outside version control.
- Team reviews open questions before agent implementation.

## 11. Open Decisions

Confirm approved data sources, qualification rules, database fields,
access roles, model providers, human approval boundaries, retention
periods, and production deployment requirements.
