import dataclasses
from datetime import timedelta
from typing import TypeVar, Callable, List, Any, Optional, Literal, Union, overload

from collect_core import CandlesCollector, InstrumentsCollector, CollectorBuilder
from data_models import CandlesModel, InstrumentsModel


@overload
async def get_collection_result(collector: CandlesCollector) -> List[CandlesModel]:
    pass


@overload
async def get_collection_result(collector: InstrumentsCollector) -> List[InstrumentsModel]:
    pass


async def get_collection_result(collector):
    return collector.serialize(await collector.read())
