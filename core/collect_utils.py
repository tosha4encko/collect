from typing import List

from collect_core import Collector
from data_models import TDataModels


async def get_collection_result[Response, Model: TDataModels](
    collector: Collector[Response, Model]
) -> List[Model]:
    return collector.serialize(await collector.read())
