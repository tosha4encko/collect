import dataclasses
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Callable, Dict

from collect_core import Meta, RunOpt, InstrumentsCollector
from data_models import InstrumentsModel
from .categories import Categories
from .client import request
from collectors_container import collectors_container
from .meta import meta_opt

_endpoint = '/v5/market/instruments-info'


@dataclasses.dataclass
class InstrumentsContext:
    market_id: int
    wallet_id: int
    contract_payout: Callable[[dict], Optional[str]]
    asset_contract: Callable[[dict], Optional[str]]
    increment_size: Callable[[dict], Optional[Decimal]]


params_opt: Dict[Categories, dict] = {
    Categories.SPOT: {
        'category': 'spot',
        'limit': 100,
    },
    Categories.LINEAR: {},
    Categories.INVERSE: {},
    Categories.OPTION: {
        'category': 'option',
        'status': 'Trading',
    },
}


context_opt: Dict[Categories, InstrumentsContext] = {
    Categories.SPOT: InstrumentsContext(
        wallet_id=2,
        market_id=1,
        contract_payout=lambda resp: None,
        asset_contract=lambda resp: None,
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["basePrecision"]),
    ),
    Categories.LINEAR: InstrumentsContext(
        wallet_id=2,
        market_id=2,
        contract_payout=lambda resp: "LINEAR",
        asset_contract=lambda resp: resp["baseCoin"],
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
    Categories.INVERSE: InstrumentsContext(
        wallet_id=2,
        market_id=2,
        contract_payout=lambda resp: 'INVERSE',
        asset_contract=lambda resp: resp["baseCoin"],
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
    Categories.OPTION: InstrumentsContext(
        wallet_id=2,
        market_id=4,
        contract_payout=lambda resp: None,
        asset_contract=lambda resp: None,
        increment_size=lambda resp: Decimal(resp["lotSizeFilter"]["qtyStep"]),
    ),
}


status_map = {"Trading": 1, "Settling": 2, "Closed": 3, "PreLaunch": 2, "Delivering": 2}


async def read(params: dict) -> List[dict]:
    response = await request(
        url=_endpoint,
        opt={"method": 'GET', "params": params},
    )
    result = response["result"]["list"]

    return result


def serialize(ctx: InstrumentsContext, meta: Meta, responses: List[dict]):
    return [InstrumentsModel(
        ts_insert=datetime.utcnow(),
        ts=datetime.utcnow(),
        exchange_id=meta.id,
        wallet_id=ctx.wallet_id,
        market_id=ctx.market_id,
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


for category in Categories:
    collectors_container.register(InstrumentsCollector(
        type='instrument',
        read=lambda: read(params_opt[category]),
        serialize=lambda responses: serialize(context_opt[category], meta_opt[category], responses),
        send=send,
        meta=meta_opt[category],
        run_opt=RunOpt(period=60, interval=timedelta(seconds=60)),
    ))
