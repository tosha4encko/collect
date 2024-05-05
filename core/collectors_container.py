from typing import List, overload, Union
from collect_core import CandleType, InstrumentType, DataTypes, \
    CANDLE_TYPE, INSTRUMENT_TYPE, Collector
from data_models import Meta, CandlesModel, InstrumentsModel, MarketTypes


class _Container:
    _candles_collectors: list[Collector[dict, CandlesModel]] = []
    _instruments_collectors: list[Collector[dict, InstrumentsModel]] = []

    @overload
    def _get_collectors_list(self,  data_type: CandleType) -> list[Collector[dict, CandlesModel]]:
        pass

    @overload
    def _get_collectors_list(self,  data_type: InstrumentType) -> list[Collector[dict, CandlesModel]]:
        pass

    def _get_collectors_list(self, data_type: CandleType | InstrumentType):
        if data_type == CANDLE_TYPE:
            return self._candles_collectors
        if data_type == INSTRUMENT_TYPE:
            return self._instruments_collectors

    @overload
    def register(self, data_type: CandleType, collector: Collector[dict, CandleType]):
        pass

    @overload
    def register(self, data_type: InstrumentType, collector: Collector[dict, InstrumentsModel]):
        pass

    def register(
        self,
        data_type: CandleType | InstrumentType,
        collector: Union[Collector, Collector[dict, InstrumentsModel]]
    ):
        current_list = self._get_collectors_list(data_type)
        current_list.append(collector)

    @overload
    def get(self, data_type: CandleType, meta: Meta) -> Collector:
        pass

    @overload
    def get(self, data_type: InstrumentType, meta: Meta) -> Collector[dict, InstrumentsModel]:
        pass

    def get(self, data_type: InstrumentType | CandleType, meta: Meta) -> Collector | Collector[dict, InstrumentsModel]:
        for collector in self._get_collectors_list(data_type):
            if (
                collector.meta.exchange == meta.exchange and
                collector.meta.market_type == meta.market_type
            ):
                return collector
        raise KeyError('No such collector')

    def get_all(
        self,
        available_types: List[DataTypes] = None,
        available_exchanges: List[str] = None,
        available_market_ids: List[str] = None,
    ):
        for current_type in [CANDLE_TYPE, INSTRUMENT_TYPE]:
            if available_types is not None and current_type not in available_exchanges:
                continue

            for collector in self._get_collectors_list(current_type):
                if available_exchanges is not None and collector.meta.exchange not in available_exchanges:
                    continue
                if available_market_ids is not None and collector.meta.market_type not in available_market_ids:
                    continue

                yield collector


collectors_container = _Container()



