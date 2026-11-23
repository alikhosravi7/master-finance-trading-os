# Trading Intelligence — Project Status

## Current milestone: Mobile-first PWA UI scaffold
- Responsive mobile-first terminal UI.
- PWA manifest, icon, and basic service-worker shell cache.
- SVG candlestick visualization with OHLC-style sample data, timeframe and symbol controls, volume bars, and conceptual ICT/SMC analysis-layer selectors.
- Existing FastAPI/PostgreSQL/Redis backend scaffold retained.

## Explicit limitations
- Chart data is illustrative and not live exchange data.
- Timeframe and analysis-layer controls are UI demonstrations; they do not query historical market data or calculate indicators/ICT structures.
- No authentication, production authorization, verified performance, or real backtest engine is implemented yet.
- PWA installation requires HTTPS or localhost. A phone cannot reach a developer's localhost without LAN hosting/tunneling and appropriate network configuration.
- Do not expose development endpoints or placeholder credentials publicly.

## Next engineering milestones
1. Run frontend build and Docker smoke tests on the target Windows machine.
2. Add authentication, RBAC, migrations, and automated tests.
3. Integrate a permitted market-data provider and normalize multi-asset OHLCV.
4. Replace the illustrative SVG with a production chart engine; implement drawing tools and real FVG/OB/liquidity/MSS overlays.
5. Implement deterministic backtesting, signal outcome tracking, and audit trails.
