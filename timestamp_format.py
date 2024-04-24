from datetime import datetime
from typing import Union


def timestamp_format(timestamp: Union[int, float]):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"),