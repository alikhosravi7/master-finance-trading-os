# Master Finance OS — Master Core V1

Local-first orchestration foundation for Windows. This is a development MVP, not a live trading system.

## What is included
- FastAPI application and health/status endpoints
- Agent registry with isolated specialist agents
- Deterministic request router
- Validation gate
- Human approval queue for sensitive actions
- SQLite audit log
- Provider-neutral AI gateway interface (stub; no API key required)
- Unit tests
- Windows setup and run scripts

## Safety boundary
V1 does not connect to MetaTrader, LiteFinance, exchange accounts, or place orders.
AI-generated changes are proposals only. Sensitive operations require explicit approval.
Do not put API keys, passwords, broker credentials, or `.env` files in audit uploads or Git.

## Requirements
- Windows 10/11
- Python 3.11+
- Internet only if you later install packages or connect an AI provider

## Quick start (PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
.\scripts\run_local.ps1
```
Open http://127.0.0.1:8000/docs

## Tests
```powershell
pytest -q
```

## API overview
- `GET /health`
- `GET /api/v1/system/status`
- `GET /api/v1/agents`
- `POST /api/v1/tasks`
- `GET /api/v1/approvals`
- `POST /api/v1/approvals/{approval_id}/decision`

Example task:
```json
{
  "task_type": "research",
  "objective": "Summarize the data quality risks in a proposed market data feed",
  "payload": {"source": "manual"}
}
```

## V1 design decisions
- Localhost binding by default
- SQLite for local MVP
- Deterministic routing before any model call
- Provider adapter is intentionally a stub until provider and credentials are selected
- No autonomous code writes or production deployments
