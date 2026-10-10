"""Contract every Orbit agent follows (Phase 1 defines it; agents are built in later phases).

Inputs : a `params` dict taken from a JobRun.input_payload.
Reads  : PostgreSQL only (companies, contacts, leads, opt_outs ...). No agent talks to another agent directly.
Writes : results back to PostgreSQL, plus an audit_log row for important actions.
Output : a small JSON summary stored in JobRun.result.
Rules  : check opt_outs before any outreach work; never send anything - sending needs human approval.
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    name: str

    @abstractmethod
    def run(self, params: dict[str, Any]) -> dict[str, Any]:
        """Do the work and return a JSON-serialisable summary."""
