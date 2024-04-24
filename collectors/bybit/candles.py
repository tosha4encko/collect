import asyncio
import dataclasses
from datetime import timedelta, datetime
from decimal import Decimal
from typing import List, override

from collectors.bybit.client import request
from collectors_container import CollectorMeta, collectors_container, CollectorBuilder, CandlesCollector, \
    InstrumentsCollector, get_collection_result
from data_models import CandlesModel, InstrumentsModel
from timestamp_format import timestamp_format

_meta = CollectorMeta(
    type='candles',
    id=1,
    class_id=1,
    period=60,
    interval=timedelta(minutes=10)
)
_endpoint = '/v5/market/kline'


@dataclasses.dataclass
class CandlesContext:
    category: str
    market_id: int
    wallet_id: int


async def read_with_instruments(instrument: InstrumentsModel):
    date_from, date_to = self.time_bracket
    limit = 200
    params = {
        "category": 'spot',
        "symbol": instrument.instrument_exch,
        "start": datetime.now() - _meta.interval,
        "end": datetime.now(),
        "interval": '1m',
        "limit": limit,
    }
    return await request(endpoint=_endpoint, opt={"method": 'GET'})


async def read_instruments(exch_id: int, class_id: int):
    instruments_collector = collectors_container.get(
        types='instruments',
        id=exch_id,
        classe_id=class_id
    )
    return await get_collection_result(instruments_collector)


async def read():
    instruments = await read_instruments(_meta.id, _meta.class_id)
    for instrument in instruments:
        read_with_instruments(instrument)




_market_map = {"spot": 1, "linear": 2, "inverse": 3}
_data_mapping = ["startTime", "openPrice", "highPrice", "lowPrice", "closePrice", "volume", "turnover"]


async def serialize(ctx: CandlesContext, data: dict):
    results = []
    instrument_exch = data["result"]["symbol"]
    data = data["result"]["list"]

    for resp in data:
        response = dict(zip(_data_mapping, resp))
        volume_base = response["volume"] if ctx.category != "inverse" else response["turnover"]
        volume_quote = response["turnover"] if ctx.category != "inverse" else response["volume"]

        result = CandlesModel(
            exchange_id=_meta.id,
            wallet_id=ctx.wallet_id,
            market_id=ctx.market_id,
            instrument_exch=instrument_exch,
            ts=timestamp_format(int(response["startTime"]) / 1000),
            type_candle=ctx.type_candle,
            open=Decimal(response["openPrice"]),
            high=Decimal(response["highPrice"]),
            low=Decimal(response["lowPrice"]),
            close=Decimal(response["closePrice"]),
            volume_base=volume_base,
            volume_quote=volume_quote,
            response=resp,
        )
        results.append(result)
    return results


async def send(data: List[CandlesModel]):
    pass


# collectors_container.register(CollectorBuilder(read=read, serialize=serialize, send=send, meta=_meta))