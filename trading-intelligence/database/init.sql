CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS instruments (
 id BIGSERIAL PRIMARY KEY, symbol VARCHAR(40) NOT NULL,
 asset_class VARCHAR(30) NOT NULL, venue VARCHAR(80),
 quote_currency VARCHAR(20), is_active BOOLEAN NOT NULL DEFAULT TRUE,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(symbol, venue)
);
CREATE TABLE IF NOT EXISTS users (
 id BIGSERIAL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE,
 display_name VARCHAR(120) NOT NULL, role VARCHAR(30) NOT NULL DEFAULT 'user',
 is_active BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS signals (
 id BIGSERIAL PRIMARY KEY, trader_id BIGINT REFERENCES users(id),
 instrument_id BIGINT REFERENCES instruments(id),
 direction VARCHAR(10) NOT NULL CHECK(direction IN ('LONG','SHORT')),
 signal_type VARCHAR(20) NOT NULL DEFAULT 'SPOT', timeframe VARCHAR(10) NOT NULL,
 entry_min NUMERIC(24,10) NOT NULL, entry_max NUMERIC(24,10) NOT NULL,
 stop_loss NUMERIC(24,10) NOT NULL, status VARCHAR(30) NOT NULL DEFAULT 'PUBLISHED',
 rationale TEXT, performance_source VARCHAR(40) NOT NULL DEFAULT 'NOT_VERIFIED',
 published_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 CHECK(entry_min <= entry_max)
);
CREATE TABLE IF NOT EXISTS signal_targets (
 id BIGSERIAL PRIMARY KEY, signal_id BIGINT NOT NULL REFERENCES signals(id) ON DELETE RESTRICT,
 target_number SMALLINT NOT NULL, price NUMERIC(24,10) NOT NULL, UNIQUE(signal_id,target_number)
);
CREATE TABLE IF NOT EXISTS signal_versions (
 id BIGSERIAL PRIMARY KEY, signal_id BIGINT NOT NULL REFERENCES signals(id) ON DELETE RESTRICT,
 version_number INTEGER NOT NULL, snapshot JSONB NOT NULL, change_reason TEXT,
 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), UNIQUE(signal_id,version_number)
);
CREATE TABLE IF NOT EXISTS signal_events (
 id BIGSERIAL PRIMARY KEY, signal_id BIGINT NOT NULL REFERENCES signals(id) ON DELETE RESTRICT,
 event_type VARCHAR(40) NOT NULL, event_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
 occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS strategies (
 id BIGSERIAL PRIMARY KEY, owner_id BIGINT REFERENCES users(id),
 name VARCHAR(160) NOT NULL, description TEXT, rules JSONB NOT NULL DEFAULT '{}'::jsonb,
 visibility VARCHAR(20) NOT NULL DEFAULT 'PRIVATE', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS backtest_jobs (
 id BIGSERIAL PRIMARY KEY, owner_id BIGINT REFERENCES users(id),
 strategy_id BIGINT REFERENCES strategies(id), instrument_id BIGINT REFERENCES instruments(id),
 timeframe VARCHAR(10) NOT NULL, start_at TIMESTAMPTZ NOT NULL, end_at TIMESTAMPTZ NOT NULL,
 config JSONB NOT NULL DEFAULT '{}'::jsonb, status VARCHAR(20) NOT NULL DEFAULT 'QUEUED',
 dataset_version VARCHAR(100), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 CHECK(start_at < end_at)
);
CREATE TABLE IF NOT EXISTS audit_logs (
 id BIGSERIAL PRIMARY KEY, actor_user_id BIGINT REFERENCES users(id),
 action VARCHAR(100) NOT NULL, entity_type VARCHAR(60) NOT NULL, entity_id BIGINT,
 details JSONB NOT NULL DEFAULT '{}'::jsonb, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_signals_published ON signals(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_instrument ON signals(instrument_id,published_at DESC);
CREATE INDEX IF NOT EXISTS idx_signal_events_signal ON signal_events(signal_id,occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_backtest_jobs_owner ON backtest_jobs(owner_id,created_at DESC);
INSERT INTO instruments(symbol,asset_class,venue,quote_currency) VALUES
('BTCUSDT','CRYPTO','BINANCE','USDT'),('ETHUSDT','CRYPTO','BINANCE','USDT'),
('EURUSD','FOREX','DEMO_FEED','USD'),('GBPUSD','FOREX','DEMO_FEED','USD'),
('XAUUSD','COMMODITY','DEMO_FEED','USD'),('USOIL','COMMODITY','DEMO_FEED','USD'),
('SPY','ETF','US_MARKET','USD'),('QQQ','ETF','US_MARKET','USD')
ON CONFLICT(symbol,venue) DO NOTHING;
