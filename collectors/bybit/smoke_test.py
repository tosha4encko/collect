from core.collect_core import INSTRUMENT_TYPE
from collectors.bybit.candles import read, serialize, context_opt
from collectors.bybit.meta_opt import meta_opt
from core.collectors_container import collectors_container
from core.data_models import MarketTypes


async def read_candle_test():
    for category in MarketTypes:
        if category != MarketTypes.OPTION:
            instruments_collector = collectors_container.get(INSTRUMENT_TYPE, meta_opt[category])
            responses = await read(context_opt[category], instruments_collector)
            print(responses)
            candles = [serialize(context_opt[category], responses)]
            print(candles)


async def bybit_test():
    await read_candle_test()
