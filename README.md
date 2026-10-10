# SoplexAI Orbit — AI Sales Intelligence & Automation

## Project Overview

SoplexAI Orbit is an AI-powered sales intelligence and workflow automation project designed to help teams organize prospect research, lead management, outreach preparation, and follow-up workflows.

This repository contains the Phase 1 planning documentation and local development setup for Orbit V1.

## Phase 1 Objectives

* Define the business context and ideal customer profile (ICP).
* Document the V1 product requirements.
* Propose the system architecture and technology stack.
* Define the initial database model.
* Identify integrations, dependencies, risks, and estimated costs.
* Establish a reproducible local development environment.
* Prepare the project for future Lead Generation Agent development.

## Technology Stack

* Python
* FastAPI
* PostgreSQL
* n8n
* Docker and Docker Compose
* Git and GitHub

## Repository Structure

```text
orbit/
├── docs/
│   ├── architecture.md
│   ├── architecture_diagram.md
│   ├── business_and_icp.md
│   ├── data_model.md
│   ├── integrations_and_costs.md
│   ├── orbit_v1_prd.md
│   ├── roadmap.md
│   ├── security_notes.md
│   └── stack_and_risks.md
├── README.md
├── .env.example
└── docker-compose.yml
```

## Local Setup

1. Clone the repository.
2. Open the project directory.
3. Create and activate a Python virtual environment if required.
4. Install the dependencies listed in the project requirements file.
5. Configure local environment variables using `.env.example`.
6. Start the services using Docker Compose:

```powershell
docker compose up --build
```

7. Open the API documentation at `http://localhost:8000/docs` when the backend is running.

## Testing

Run the project's documented test command from the project directory. Confirm that the backend tests pass and that the required services start successfully.

## Documentation

The `docs/` directory contains the product requirements, business and ICP summary, architecture, data model, integration considerations, security notes, risks, and roadmap.

## Security Notes

* Never commit real credentials or secrets.
* Keep `.env` out of version control.
* Use `.env.example` to document required configuration variables without exposing secret values.
* Require human review and approval before outreach is sent.
* Follow applicable laws and the terms of the platforms used for prospect research and outreach.

## Scope

Phase 1 focuses on requirements, architecture, documentation, and local setup. It does not claim that every planned AI agent, dashboard, or external integration has already been implemented.

## Future Work

The next phase will prepare and develop the Lead Generation Agent, following review of the requirements, architecture, data model, and security considerations.
