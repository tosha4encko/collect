import dataclasses
import json
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Union


class MarketTypes(Enum):
    SPOT = 'spot'
    LINEAR = 'linear'
    INVERSE = 'inverse'
    OPTION = 'option'


@dataclasses.dataclass
class Meta:
    exchange: str
    market_type: MarketTypes


class DataType:
    @abs
    def serialize(self) -> dict:
        pass

    @abs
    def deserialize(self):
        pass


@dataclass
class InstrumentsModel(DataType):
    ts: datetime
    ts_insert: datetime
    status_id: int
    instrument_exch: str
    asset_base_exch: str
    asset_quote_exch: str
    response: dict
    category: Optional[str] = None
    asset_margin_exch: Optional[str] = None
    contract_type: Optional[str] = None
    contract_expiration: Optional[str] = None
    contract_payout: Optional[str] = None
    asset_contract: Optional[str] = None
    contract_size: Optional[Decimal] = None
    tick_size: Optional[Decimal] = None
    increment_size: Optional[Decimal] = None


@dataclass
class CandlesModel:
    instrument_exch: str
    type_candle: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume_base: Decimal
    volume_quote: Decimal
    response: dict
    ts: datetime
    trade_count: Optional[int] = None
    ts_inserted: datetime = field(default_factory=datetime.utcnow)

    def serialize(self):
        candle = self.__dict__
        candle["ts"] = self.ts.timestamp()
        candle["ts_inserted"] = self.ts_inserted.timestamp()

        return json.dumps(candle)

    @staticmethod
    def deserialize(msg: bytes):
        candle = json.loads(msg)
        return CandlesModel(
            instrument_exch=candle["instrument_exch"],
            type_candle=candle["type_candle"],
            open=Decimal(candle["open"]),
            high=Decimal(candle["high"]),
            low=Decimal(candle["low"]),
            close=Decimal(candle["close"]),
            volume_base=Decimal(candle["volume_base"]),
            volume_quote=Decimal(candle["volume_quote"]),
            response=candle["response"],
            ts=datetime.fromtimestamp(candle["ts"]),
            trade_count=candle.get("trade_count"),
            ts_inserted=datetime.fromtimestamp(candle["ts_inserted"]),
        )


TDataModels = Union[CandlesModel, InstrumentsModel]
