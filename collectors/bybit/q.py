from asyncio import gather
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

import pandas as pd

import exchanges.data_collectors.Bybit as collectors
from exchanges.data_collectors.Base.data_models import CandlesModel
from exchanges.data_collectors.Base.data_types import BaseCandles
from exchanges.data_collectors.Base.helper import UsedInstrumentsChecker
from exchanges.data_collectors.helpers import dt_to_ts, ts_to_dt


_market_map = {"spot": 1, "linear": 2, "inverse": 3}


class Candles(BaseCandles):
    def __init__(self, only_used=False, interval=60, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data_type = "candles" if interval == 60 else 'candles_1m'
        self.exchange_id = 14
        self.exchange_class_id = 18
        self.wallet_id = 2
        self.endpoint = "/v5/market/kline"
        self.interval = interval
        self.only_used = only_used
        self.used_instruments_checker = UsedInstrumentsChecker([self.exchange_id], [self.wallet_id], [*_market_map.values()])

    async def get_instruments(self):
        collector = collectors.Instruments(self.url, self.client, self.throttler, self.account)

        categories = ("spot", "linear", "inverse")
        tasks = [collector._get_instruments(category) for category in categories]
        responses = await gather(*tasks)
        results = []
        for resp in responses:
            results.append({resp[1]: [i["symbol"] for i in resp[0]]})
        return results

    async def get_candle(self, category, instr):
        date_from, date_to = self.time_bracket
        limit = 200
        params = {
            "category": category,
            "symbol": instr,
            "start": int(dt_to_ts(date_from)),
            "end": int(dt_to_ts(date_to)),
            "interval": self.interval,
            "limit": limit,
        }
        candles = []
        while True:
            responses, status, ts = await self.make_request(
                self.url, self.endpoint, self.throttler, self.exchange_class_id, self.account, params=params
            )
            if status == 200:
                if responses:
                    data = responses["result"]["list"]
                    if self.time_bracket and len(data) == limit:
                        oldest_ts = data[-1][0]
                        oldest_dt = ts_to_dt(oldest_ts)
                        if date_from < oldest_dt:
                            params["end"] = int(oldest_ts)
                            responses["result"]["list"] = responses["result"]["list"][:-1]
                            results = await self.get_serialized_results(responses, category)
                            candles.extend(results)
                            continue
                    results = await self.get_serialized_results(responses, category)
                    candles.extend(results)

            return candles

    async def get_candles(self):
        instruments = await self.get_instruments()
        tasks = []
        for instrs_info in instruments:
            for category, instrs in instrs_info.items():
                for instr in instrs:
                    if self.only_used and not await self.used_instruments_checker.check(instr):
                        continue
                    tasks.append(self.get_candle(category, instr))
        responses = await gather(*tasks)
        results = []
        for res in responses:
            results.extend(res)
        await self.send(results)

    async def get_serialized_results(self, responses, category):
        results = []
        data_mapping = [
            "startTime",
            "openPrice",
            "highPrice",
            "lowPrice",
            "closePrice",
            "volume",
            "turnover",
        ]
        instrument_exch = responses["result"]["symbol"]
        responses = responses["result"]["list"]

        for resp in responses:
            response = dict(zip(data_mapping, resp))

            market_id = _market_map[category]
            if category == "spot":
                volume_base = response["volume"]
                volume_quote = response["turnover"]
            elif category == "linear":
                volume_base = response["volume"]
                volume_quote = response["turnover"]
            elif category == "inverse":
                volume_base = response["turnover"]
                volume_quote = response["volume"]

            if self.interval == 60:
                type_candle = "1h"
            if self.interval == 1:
                type_candle = "1m"

            ts = datetime.fromtimestamp(int(response["startTime"]) / 1000).strftime("%Y-%m-%d %H:%M:%S.%f")

            _open = Decimal(response["openPrice"])
            high = Decimal(response["highPrice"])
            low = Decimal(response["lowPrice"])
            close = Decimal(response["closePrice"])

            result = CandlesModel(
                exchange_id=self.exchange_id,
                wallet_id=self.wallet_id,
                market_id=market_id,
                instrument_exch=instrument_exch,
                ts=ts,
                type_candle=type_candle,
                open=_open,
                high=high,
                low=low,
                close=close,
                volume_base=volume_base,
                volume_quote=volume_quote,
                response=resp,
            )
            results.append(result.__dict__)
        return results
