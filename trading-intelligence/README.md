# Trading Intelligence — Local MVP Foundation

Initial runnable scaffold:
- Next.js dashboard
- FastAPI backend
- PostgreSQL + TimescaleDB
- Redis
- Docker Compose
- Seed market instruments
- Signal create/list API
- Signal versions and event records

**Not production-ready:** no real authentication, live market feed, verified P&L engine, or functioning backtester is included yet. Do not expose this development configuration to the public internet.

## Windows requirements
- Windows 10/11 with virtualization enabled
- Docker Desktop running with Linux containers
- 8 GB RAM recommended

## Run
Open PowerShell in the extracted `trading-intelligence` folder:
```powershell
docker compose up --build -d
docker compose ps
```
Open:
- Dashboard: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Stop
```powershell
docker compose down
```
Delete all local database data (destructive):
```powershell
docker compose down -v
```

## Test signal creation
Use Swagger at http://localhost:8000/docs, POST `/api/v1/signals`:
```json
{
  "symbol":"BTCUSDT","asset_class":"CRYPTO","venue":"BINANCE",
  "direction":"LONG","signal_type":"FUTURES","timeframe":"15m",
  "entry_min":"92000","entry_max":"92200","stop_loss":"91500",
  "take_profits":["93500","94800","96000"],
  "rationale":"Development test only"
}
```
Refresh dashboard to see the saved signal.

## Troubleshooting
- Start Docker Desktop and wait for engine readiness.
- Ports 3000, 5432, 6379, 8000 must be free.
- Inspect logs: `docker compose logs -f api`
- Health check: `http://localhost:8000/health`
- If the database initialization needs to be rerun, note that `docker compose down -v` deletes local data.

## Security
Credentials are local placeholders. Do not deploy publicly. Before deployment add authentication, secrets management, HTTPS, migrations, backups, authorization tests, monitoring, rate limiting and legal review. Never put exchange API secrets in frontend code.

## Next milestones
1. Alembic migrations.
2. Authentication and RBAC.
3. Trader verification and audit protections.
4. Licensed market-data adapters.
5. Signal outcome reconstruction.
6. Strategy backtesting with realistic fills, fees, spread and slippage.
7. Automated tests and CI.

## Mobile PWA preview

The web client is configured as a mobile-first Progressive Web App (PWA). On Android, open the site in Chrome and choose **Install app** or **Add to Home screen** from the browser menu. The PWA manifest, SVG app icon, and basic service worker shell cache are included.

The candlestick panel is an illustrative SVG chart driven by bundled sample OHLC values. It is not connected to an exchange feed and must not be used for trading decisions. The timeframe and instrument selectors currently change the demonstration view only. A production chart should be connected to a licensed/authorized market-data provider and a dedicated charting engine before live use.

### Mobile access

The PWA is installable only after the web app is served from `localhost` or a secure HTTPS origin. For access from a phone on the same Wi-Fi network during local development, configure the host firewall and publish the web container on a reachable LAN address; for remote access, use a secured HTTPS deployment. Do not expose the current development API or database directly to the public internet.
