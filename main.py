import asyncio

from collectors_container import CollectorBuilder, collectors_container
from collectors import *


async def collect(collector: CollectorBuilder):
    while True:
        exchange_data = await collector.read()
        serialized_data = collector.serialize(exchange_data)
        await collector.send(serialized_data)

        await asyncio.sleep(collector.run_opt.period)


async def run_collect():
    tasks = []
    for collector in collectors_container.get_all():
        tasks.append(collect(collector))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run_collect())
