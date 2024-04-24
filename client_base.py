import asyncio
import json
from typing import TypedDict, Optional, Literal, Callable, Coroutine
from asyncio import sleep, Semaphore

from aiohttp import ClientSession, ClientResponse


class RequestOpt(TypedDict):
    method: Optional[str]
    body: Optional[dict]
    headers: Optional[dict]
    method: Optional[Literal['GET', 'POST']]
    auth: Optional[dict]
    params: Optional[dict]
    session: Optional[ClientSession]
    proxi: Optional[str]


RequestFunctType = Callable[
    [str, RequestOpt, Optional[ClientSession]],
    Coroutine[None, None, ClientResponse]
]


async def base_request(url: str, opt: RequestOpt, session: Optional[ClientSession] = None):
    current_session = session or ClientSession()
    try:
        async with current_session.request(url=url, **opt) as response:
            data = await response.read()
            if response.status == 200:
                return json.loads(data)
            raise Exception(data)
    finally:
        if session is None:
            await current_session.close()  # close session only if session created in this func


def create_request_to_source(source: str, request_cb: RequestFunctType) -> RequestFunctType:
    def request(url: str, opt: RequestOpt, session: Optional[ClientSession] = None):
        return request_cb(source + url, opt, session)

    return request


def create_request_with_throttle(interval_ms: int, volume: int, request_cb: RequestFunctType) -> RequestFunctType:
    semaphore = Semaphore(volume)

    async def unlock():
        try:
            await sleep(interval_ms)
        finally:
            semaphore.release()

    async def request(url: str, opt: RequestOpt, session: Optional[ClientSession] = None):
        await semaphore.acquire()
        try:
            return await request_cb(url, opt, session)
        finally:
            asyncio.create_task(unlock())

    return request


