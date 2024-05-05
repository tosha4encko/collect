import asyncio

from core.collect_core import Collector
from core.collectors_container import collectors_container


async def collect(collector: Collector):
    while True:
        # place for log
        exchange_data = await collector.read()
        # place for log
        serialized_data = collector.serialize(exchange_data)
        # place for log
        await collector.send(serialized_data)
        # place for log

        await asyncio.sleep(collector.run_opt.period)


async def run_collect():
    tasks = []
    for collector in collectors_container.get_all():
        tasks.append(collect(collector))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run_collect())
