import dataclasses
from datetime import timedelta
from typing import TypeVar, Callable, Optional, Literal, Union, List, Coroutine

from data_models import TDataModels, Meta

CANDLE_TYPE: Literal['candle'] = 'candle'
INSTRUMENT_TYPE: Literal['instrument'] = 'instrument'

DataTypes = Union[type(CANDLE_TYPE), type(INSTRUMENT_TYPE)]

ExchangeResponse = TypeVar('ExchangeResponse')
SerializeResponse = TypeVar('SerializeResponse', bound=TDataModels)

ReadCB = Callable[[], Coroutine[None, None, List[ExchangeResponse]]]
SerializedCB = Callable[[List[ExchangeResponse]], List[SerializeResponse]]
SendCB = Callable[[List[SerializeResponse]], Coroutine[None, None, None]]


@dataclasses.dataclass
class RunOpt:
    period: int
    interval: Optional[timedelta] = None


@dataclasses.dataclass
class Collector[Response, Model: TDataModels]:
    read: ReadCB
    serialize: SerializedCB[Response, Model]
    send: SendCB[Model]

    meta: Meta
    run_opt: RunOpt
