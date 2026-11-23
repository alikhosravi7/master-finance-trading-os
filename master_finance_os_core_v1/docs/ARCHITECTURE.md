# Master Core V1 — Architecture

## Components
1. API layer: FastAPI routes and request schemas.
2. Orchestrator: deterministic routing and workflow control.
3. Agent registry: maps task types to specialist agents.
4. AI gateway: provider-neutral adapter; currently a safe stub.
5. Quality gate: validates agent result structure and status.
6. Approval manager: records pending approvals for sensitive task classes.
7. Audit store: append-only event records in local SQLite.

## Trust boundaries
- AI output is untrusted input.
- Agents do not receive broker credentials.
- No module can place orders in V1.
- Approval is an explicit human action.
- The local API binds to 127.0.0.1 by default.
- Secrets are loaded from environment variables and must never be committed.

## Next engineering milestones
- Add authentication even for LAN exposure; keep localhost-only until then.
- Add structured logging, migrations, backup/restore and retention policy.
- Add provider adapters only after provider selection and secret handling.
- Add contract tests for each agent.
- Integrate existing project modules only after inventory and code review.
- Add MT5 connector in a separate process with strict risk and order permission gates.
