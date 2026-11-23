# Master Finance OS — Integrated Recovery Build

Recovered source packages integrated on 2026-11-24. This is a source consolidation, not a production release.

## Modules
- `master_finance_os_core_v1/`: FastAPI orchestration core, agent registry, quality engine, SQLite persistence, tests.
- `master_finance_trading_os/`: Persian RTL mobile-first PWA shell with journal, backtest records, strategy registry and TradingView embed.
- `trading-intelligence/`: Next.js/FastAPI/PostgreSQL application and mobile PWA assets.

## Run / test
- Core: `python -m pip install -r master_finance_os_core_v1/requirements.txt` then `python -m pytest master_finance_os_core_v1/tests -q`
- Trading Intelligence: `docker compose -f trading-intelligence/docker-compose.yml up --build` (Docker runtime not verified here).
- Mobile shell: serve `master_finance_trading_os/` over HTTPS to enable PWA install.

## Important limitations
- The mobile shell stores user records in browser localStorage; it is not synced to the API.
- No broker order execution is implemented. MT5 connector is a separate read-only package and is not bundled here.
- Market feeds and external API integrations require separate configuration and validation.
- Do not commit credentials, API keys, broker logins, or personal trading records.
- Not production-ready; perform Windows/browser/Docker/MT5 runtime tests before operational use.
