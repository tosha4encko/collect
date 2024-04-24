from typing import List, overload
from collect_core import CollectorBuilder, CandleType, CandlesCollector, InstrumentsCollector, InstrumentTypes


class _Container:
    _collectors_list: List[CollectorBuilder] = []

    def register(self, collector: CollectorBuilder):
        self._collectors_list.append(collector)

    @overload
    def get_one(self, available_type: CandleType, id: int, class_id: int) -> CandlesCollector:
        pass

    def get_one(self, available_type: InstrumentTypes, id: int, class_id: int) -> InstrumentsCollector:
        pass

    def get(self, type, id, class_id):
        for collector in self._collectors_list:
            meta = collector.meta
            if meta.type == type and meta.id == id and meta.class_id == class_id:
                return collector
        raise KeyError('No such collector')

    def get_all(
        self,
        available_types: List[str] = None,
        available_ids: List[str] = None,
        available_classes_ids: List[str] = None,
    ):
        for collector in self._collectors_list:
            if available_types is not None and collector.meta.type not in available_types:
                continue
            if available_ids is not None and collector.meta.id not in available_ids:
                continue
            if available_classes_ids is not None and collector.meta.class_id not in available_classes_ids:
                continue

            yield collector


collectors_container = _Container()



