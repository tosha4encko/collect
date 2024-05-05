import dataclasses
from typing import Union, TypedDict, Literal, Tuple, TypeVar, Dict, Callable, Any, overload


class CandlesModel:
    pass

class InstrumentsModel:
    pass



CandleTypeName = Literal['candle']
InstrumentsTypeName = Literal['instruments']

class C(TypedDict):
    type: CandleTypeName
    model: CandlesModel

class I(TypedDict):
    type: InstrumentsTypeName
    model: InstrumentsModel


P = TypeVar('P', bound=Union[C, I])

GetC = Callable[[CandleTypeName], CandlesModel]
GetI = Callable[[InstrumentsTypeName], InstrumentsModel]


@overload
def get_meta(type: CandleTypeName) -> CandlesModel:
    pass

@overload
def get_meta(type: InstrumentsTypeName) -> InstrumentsModel:
    pass

def get_meta(type):
    if type == CandleTypeName:
        return CandlesModel()
    if type == InstrumentsTypeName:
        return InstrumentsModel()

a = get_meta('instruments')


# Создание сопоставления между типами данных и их коллекциями
type_mapping: CollectTypeMapping = {'CandlesModel': 'candle', 'InstrumentsModel': 'instrument'}

# Использование функции
registr(CandlesModel(), 'candle')  # Корректно
registr(InstrumentsModel(), 'instrument')  # Корректно
registr(CandlesModel(), 'instrument')  # Ошибка типа
registr(InstrumentsModel(), 'candle')  # Ошибка типа
