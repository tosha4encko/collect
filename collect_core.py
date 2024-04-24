import dataclasses
from datetime import timedelta
from typing import TypeVar, Callable, Any, Optional, Literal, Union, List, Coroutine

from data_models import CandlesModel, InstrumentsModel


ExchangeType = TypeVar('ExchangeType')
SerializedType = Union[CandlesModel, InstrumentsModel]
ReadCB = Callable[[], Coroutine[None, None, List[ExchangeType]]]

SerializedCandles = Callable[[List[ExchangeType]], CandlesModel]
SerializedInstruments = Callable[[List[ExchangeType]], List[InstrumentsModel]]

SendCandles = Callable[[CandlesModel], Any]
SendInstruments = Callable[[List[InstrumentsModel]], Any]


@dataclasses.dataclass
class Meta:
    id: int
    class_id: int


@dataclasses.dataclass
class RunOpt:
    period: int
    interval: Optional[timedelta] = None


CandleType = Literal['candle']
InstrumentTypes = Literal['instrument']


@dataclasses.dataclass
class CandlesCollector:
    type: CandleType
    read: ReadCB
    serialize: SerializedCandles
    send: SendCandles
    run_opt: RunOpt
    meta: Meta


@dataclasses.dataclass
class InstrumentsCollector:
    type: InstrumentTypes
    read: ReadCB
    serialize: SerializedInstruments
    send: SendInstruments
    run_opt: RunOpt
    meta: Meta


CollectorBuilder = Union[CandlesCollector, InstrumentsCollector]

