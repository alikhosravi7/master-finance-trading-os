from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class SignalCreate(BaseModel):
    trader_id: int | None = None
    symbol: str = Field(min_length=2, max_length=40)
    asset_class: str = Field(min_length=2, max_length=30)
    venue: str | None = None
    direction: Literal["LONG", "SHORT"]
    signal_type: Literal["SPOT", "FUTURES", "FOREX", "STOCK", "CFD"] = "SPOT"
    timeframe: str = Field(min_length=1, max_length=10)
    entry_min: Decimal
    entry_max: Decimal
    stop_loss: Decimal
    take_profits: list[Decimal] = Field(min_length=1, max_length=10)
    rationale: str | None = None

    @model_validator(mode="after")
    def validate_prices(self):
        if self.entry_min > self.entry_max:
            raise ValueError("entry_min must be <= entry_max")
        if any(p <= 0 for p in [self.entry_min, self.entry_max, self.stop_loss, *self.take_profits]):
            raise ValueError("All prices must be positive")
        return self

class SignalOut(BaseModel):
    id: int
    symbol: str
    asset_class: str
    direction: str
    signal_type: str
    timeframe: str
    entry_min: Decimal
    entry_max: Decimal
    stop_loss: Decimal
    status: str
    rationale: str | None
    performance_source: str
    published_at: datetime
    take_profits: list[Decimal] = []
