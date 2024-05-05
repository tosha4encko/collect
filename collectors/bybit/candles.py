from decimal import Decimal
from typing import *
import asyncio
import dataclasses
from datetime import datetime, timedelta

from core.collect_core import RunOpt, INSTRUMENT_TYPE, Collector, CANDLE_TYPE
from core.collect_utils import get_collection_result
from collectors.bybit.client import request
from collectors.bybit.meta_opt import meta_opt
from core.collectors_container import collectors_container
from core.data_models import InstrumentsModel, CandlesModel, MarketTypes
from timestamp_format import timestamp_format
from send.send_to_kafka import create_kafka_sender


_endpoint = '/v5/market/kline'
runOpt = RunOpt(period=60, interval=timedelta(minutes=60))


@dataclasses.dataclass
class CandlesCtx:
    volume_base: Callable[[dict], str]
    volume_quote: Callable[[dict], str]
    category: MarketTypes


context_opt: Dict[MarketTypes, CandlesCtx] = {
    MarketTypes.SPOT: CandlesCtx(
        category=MarketTypes.SPOT,
        volume_base=lambda response: response["volume"],
        volume_quote=lambda response: response["turnover"],
    ),
    MarketTypes.LINEAR: CandlesCtx(
        category=MarketTypes.LINEAR,
        volume_base=lambda response: response["volume"],
        volume_quote=lambda response: response["turnover"],
    ),
    MarketTypes.INVERSE: CandlesCtx(
        category=MarketTypes.INVERSE,
        volume_base=lambda response: response["turnover"],
        volume_quote=lambda response: response["volume"],
    ),
}


async def read_with_instruments(ctx: CandlesCtx, interval: timedelta, instrument: InstrumentsModel):
    params = {
        "category": ctx.category.value,
        "symbol": instrument.instrument_exch,
        "start": int((datetime.now() - interval).timestamp()*1000),
        "end": int(datetime.now().timestamp()*1000),
        "interval": 60,
        "limit": 200,
    }

    return await request(_endpoint, opt={"method": 'GET', 'params': params})


async def read(ctx: CandlesCtx, interval: timedelta, instr_collector: Collector[dict, InstrumentsModel]) -> List[dict]:
    instruments = await get_collection_result(instr_collector)
    tasks = [read_with_instruments(ctx, interval, instrument) for instrument in instruments[:10]]
    res: List[dict] = [*await asyncio.gather(*tasks)]

    return res


_data_mapping = ["startTime", "openPrice", "highPrice", "lowPrice", "closePrice", "volume", "turnover"]


def serialize(ctx: CandlesCtx, data: List[dict]):
    results = []
    for item in data:
        instrument_exch = item["result"]["symbol"]
        responses = item["result"]["list"]
        for resp in responses:
            response = dict(zip(_data_mapping, resp))
            result = CandlesModel(
                instrument_exch=instrument_exch,
                ts=timestamp_format(int(response["startTime"]) / 1000),
                type_candle='1h',
                open=Decimal(response["openPrice"]),
                high=Decimal(response["highPrice"]),
                low=Decimal(response["lowPrice"]),
                close=Decimal(response["closePrice"]),
                volume_base=Decimal(ctx.volume_base(response)),
                volume_quote=Decimal(ctx.volume_quote(response)),
                response=resp,
            )
            results.append(result)
    return results


sender = create_kafka_sender()


for category in MarketTypes:
    if category != MarketTypes.OPTION:
        instruments_collector = collectors_container.get(INSTRUMENT_TYPE, meta_opt[category])
        collectors_container.register(CANDLE_TYPE, Collector(
            read=lambda cat=category: read(context_opt[cat], runOpt.interval, instruments_collector),
            serialize=lambda responses, cat=category: serialize(context_opt[cat], responses),
            send=sender,
            meta=meta_opt[category],
            run_opt=runOpt,
        ))
