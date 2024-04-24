from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class AssetsModel:
    exchange_id: int
    asset_exch: str
    name: str
    chain_exch: str
    can_deposit: bool
    can_withdraw: bool
    response: dict
    ts: datetime
    type_fee_id: int = 0
    fee_fixed: Optional[Decimal] = None
    fee_min: Optional[Decimal] = None
    fee_max: Optional[Decimal] = None
    withdraw_min: Optional[Decimal] = None
    withdraw_max: Optional[Decimal] = None


@dataclass
class TickersModel:
    exchange_id: int
    market_id: int
    instrument_exch: str
    ask: Decimal
    bid: Decimal
    last: Decimal
    response: dict
    ts: datetime
    mark: Optional[Decimal] = None


@dataclass
class AliveCheckModel:
    ts: datetime
    exchange_id: int
    is_alive: bool
    info: Optional[str] = None


@dataclass
class InstrumentsModel:
    ts: datetime
    ts_insert: datetime
    exchange_id: int
    wallet_id: int
    market_id: int
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
class FuturesBasisModel:
    exchange_id: int
    market_id: int
    instrument_exch: str
    ts: datetime
    response: dict
    mark: Optional[Decimal] = None
    index: Optional[Decimal] = None
    basis_rate: Optional[Decimal] = None
    funding_prev: Optional[Decimal] = None
    funding_next: Optional[Decimal] = None
    volume_24h: Optional[Decimal] = None
    oi: Optional[Decimal] = None


@dataclass
class CoinGeckoModel:
    id_coingecko: str
    asset_exch: str
    name: str
    price: Decimal
    market_cap: Decimal
    market_cap_rank: int
    fully_diluted_valuation: Decimal
    vol_24h: Decimal
    circulating_supply: Decimal
    total_supply: Decimal
    ts: datetime
    response: dict


@dataclass
class InstrumentsMappingModel:
    exchange_id: int
    instrument_exch: str
    instrument_bender: str
    asset_base_core: str
    asset_quote_core: str
    response: dict
    ts: datetime
    ts_insert: datetime


@dataclass
class CandlesModel:
    exchange_id: int
    wallet_id: int
    market_id: int
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


@dataclass
class StakingRatesMappingModel:
    account_id: int
    ts: datetime
    product_exch: str
    asset_exch: str
    amount_min: Decimal
    amount_max: Decimal
    apy: Decimal
    response: dict
    can_autorenew: Optional[bool] = None
    can_redeem: Optional[bool] = None
    duration_days: Optional[int] = None
