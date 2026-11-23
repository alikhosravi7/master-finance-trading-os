import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db, check_database
from .schemas import SignalCreate

app = FastAPI(
    title="Trading Intelligence API",
    version="0.1.0",
    description="Initial local MVP API. Market data and performance are not yet live-verified."
)
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"], allow_headers=["*"]
)

@app.get("/health")
def health():
    try:
        check_database()
        return {"status": "ok", "database": "connected", "environment": os.getenv("APP_ENV", "development")}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {type(exc).__name__}")

@app.get("/api/v1/markets")
def list_markets(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT id,symbol,asset_class,venue,quote_currency,is_active
        FROM instruments WHERE is_active=TRUE ORDER BY asset_class,symbol
    """)).mappings().all()
    return [dict(row) for row in rows]

@app.get("/api/v1/signals")
def list_signals(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    rows = db.execute(text("""
        SELECT s.id,i.symbol,i.asset_class,s.direction,s.signal_type,s.timeframe,
               s.entry_min,s.entry_max,s.stop_loss,s.status,s.rationale,
               s.performance_source,s.published_at
        FROM signals s JOIN instruments i ON i.id=s.instrument_id
        ORDER BY s.published_at DESC LIMIT :limit
    """), {"limit": limit}).mappings().all()
    result = []
    for row in rows:
        item = dict(row)
        item["take_profits"] = db.execute(
            text("SELECT price FROM signal_targets WHERE signal_id=:sid ORDER BY target_number"),
            {"sid": item["id"]}
        ).scalars().all()
        result.append(item)
    return result

@app.post("/api/v1/signals", status_code=201)
def create_signal(payload: SignalCreate, db: Session = Depends(get_db)):
    instrument = db.execute(text("""
        SELECT id FROM instruments
        WHERE symbol=:symbol AND asset_class=:asset_class
          AND ((venue IS NULL AND :venue IS NULL) OR venue=:venue)
        LIMIT 1
    """), {"symbol": payload.symbol.upper(), "asset_class": payload.asset_class.upper(), "venue": payload.venue}).scalar()
    if instrument is None:
        raise HTTPException(status_code=404, detail="Instrument not found in catalog.")
    signal_id = db.execute(text("""
        INSERT INTO signals(trader_id,instrument_id,direction,signal_type,timeframe,
          entry_min,entry_max,stop_loss,rationale,status,performance_source)
        VALUES(:trader_id,:instrument_id,:direction,:signal_type,:timeframe,
          :entry_min,:entry_max,:stop_loss,:rationale,'PUBLISHED','NOT_VERIFIED')
        RETURNING id
    """), {
        "trader_id": payload.trader_id, "instrument_id": instrument,
        "direction": payload.direction, "signal_type": payload.signal_type,
        "timeframe": payload.timeframe, "entry_min": payload.entry_min,
        "entry_max": payload.entry_max, "stop_loss": payload.stop_loss,
        "rationale": payload.rationale
    }).scalar_one()
    for n, price in enumerate(payload.take_profits, start=1):
        db.execute(text("""
            INSERT INTO signal_targets(signal_id,target_number,price)
            VALUES(:sid,:n,:price)
        """), {"sid": signal_id, "n": n, "price": price})
    db.execute(text("""
        INSERT INTO signal_versions(signal_id,version_number,snapshot,change_reason)
        VALUES(:sid,1,CAST(:snapshot AS jsonb),'Initial publication')
    """), {"sid": signal_id, "snapshot": payload.model_dump_json()})
    db.execute(text("""
        INSERT INTO signal_events(signal_id,event_type,event_payload)
        VALUES(:sid,'PUBLISHED','{}'::jsonb)
    """), {"sid": signal_id})
    db.commit()
    return {"id": signal_id, "status": "PUBLISHED", "performance_source": "NOT_VERIFIED"}

@app.get("/api/v1/backtests/status")
def backtest_status():
    return {"status": "NOT_IMPLEMENTED", "message": "Backtesting is planned; no performance is fabricated."}
