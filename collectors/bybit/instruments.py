import dataclasses
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Callable, Dict

from core.collect_core import RunOpt, INSTRUMENT_TYPE, Collector
from core.data_models import InstrumentsModel, MarketTypes
from .client import request
from core.collectors_container import collectors_container
from .meta_opt import meta_opt

_endpoint = '/v5/market/instruments-info'


@dataclasses.dataclass
class InstrumentsContext:
    contract_payout: Callable[[dict], Optional[str]]
    asset_contract: Callable[[dict], Optional[str]]
    increment_size: Callable[[dict], Optional[Decimal]]


params_opt: Dict[MarketTypes, dict] = {
    MarketTypes.SPOT: {
        'category': 'spot',
        'limit': 100,
    },
    MarketTypes.LINEAR: {
        'category': 'linear',
    },
    MarketTypes.OPTION: {
        'category': 'option',
        'status': 'Trading',
    },
    MarketTypes.INVERSE: {
        'category': 'inverse',
    },
}


context_opt: Dict[MarketTypes, InstrumentsContext] = {
    MarketTypes.SPOT: InstrumentsContext(
        contract_payout=lambda resp: None,
        asset_contract=lambda resp: None,
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["basePrecision"]),
    ),
    MarketTypes.LINEAR: InstrumentsContext(
        contract_payout=lambda resp: "LINEAR",
        asset_contract=lambda resp: resp["baseCoin"],
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
    MarketTypes.INVERSE: InstrumentsContext(
        contract_payout=lambda resp: 'INVERSE',
        asset_contract=lambda resp: resp["baseCoin"],
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
    MarketTypes.OPTION: InstrumentsContext(
        contract_payout=lambda resp: None,
        asset_contract=lambda resp: None,
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
}


status_map = {"Trading": 1, "Settling": 2, "Closed": 3, "PreLaunch": 2, "Delivering": 2}


async def read(params: dict) -> List[dict]:
    response = await request(
        endpoint=_endpoint,
        opt={"method": 'GET', "params": params},
    )
    result = response["result"]["list"]

    return result


def serialize(ctx: InstrumentsContext, responses: List[dict]):
    return [InstrumentsModel(
        ts_insert=datetime.now(),
        ts=datetime.now(),
        contract_payout=ctx.contract_payout(response),
        asset_contract=ctx.asset_contract(response),
        status_id=status_map[response["status"]],
        increment_size=ctx.increment_size(response),
        contract_size=Decimal(1),
        instrument_exch=response["symbol"],
        asset_base_exch=response["baseCoin"],
        asset_quote_exch=response["quoteCoin"],
        asset_margin_exch=response.get("settleCoin"),
        contract_type=response.get("contractType"),
        contract_expiration=response.get("deliveryTime"),
        tick_size=Decimal(response["priceFilter"]["tickSize"]),
        response=response,
    ) for response in responses]


async def send(instruments: list[InstrumentsModel]):
    print(instruments)


for category in MarketTypes:
    collectors_container.register(INSTRUMENT_TYPE, Collector(
        read=lambda cat=category: read(params_opt[cat]),
        serialize=lambda responses, cat=category: serialize(context_opt[cat], responses),
        send=send,
        meta=meta_opt[category],
        run_opt=RunOpt(period=60, interval=timedelta(seconds=60)),
    ))
