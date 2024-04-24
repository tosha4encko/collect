from typing import Dict

from collect_core import Meta
from collectors.bybit.instruments import Categories

meta_opt: Dict[Categories, Meta] = {
    Categories.SPOT:  Meta(id=1, class_id=1),
    Categories.LINEAR: Meta(id=1, class_id=2),
    Categories.INVERSE: Meta(id=1, class_id=3),
    Categories.OPTION: Meta(id=1, class_id=4),
}