import json
from typing import TypedDict, Optional, Literal, Callable, Coroutine

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
        if session is None: # close session only if session created in this func
            await current_session.close()


def create_request_to_source(source: str, request_cb: RequestFunctType) -> RequestFunctType:
    def request(endpoint: str, opt: RequestOpt, session: Optional[ClientSession] = None):
        return request_cb(source + endpoint, opt, session)

    return request



