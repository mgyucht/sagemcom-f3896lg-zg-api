from types import TracebackType
from typing import Optional, Any, Type
import aiohttp
import aiohttp.typedefs
import logging

from .model import LoginResponseModel, NetworkHostsModel

_LOGGER = logging.getLogger(__name__)

API_BASE = "/rest/v1"

class SagemcomF3896LGApi:
    def __init__(self, password: str, router_endpoint: str) -> None:
        self._password = password
        self._router_endpoint = router_endpoint
        self._session = None
        self._token = None

    async def close(self):
        if self._session is not None:
            await self.logout()
            await self._session.close()

    async def __aenter__(self) -> 'SagemcomF3896LGApi':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]) -> None:
        await self.close()

    def _request(self, method: str, endpoint: str, params: aiohttp.typedefs.Query = None, json: Any = None, session: aiohttp.ClientSession = None) -> aiohttp.ClientResponse:
        if session is None:
            session = self._session
        return session.request(method, f"http://{self._router_endpoint}{API_BASE}{endpoint}", params=params, json=json)

    async def login(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with self._request('POST', "/user/login", json={'password': self._password}, session=session) as response:
                if response.status == 201:
                    json = await response.json()
                    data = LoginResponseModel(**json)
                    self._token = data.created
                    self._session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {data.created.token}'})
                    return True
                else:
                    body = await response.text()
                    _LOGGER.warning(f"failed to login (status code {response.status}): {body}")
                    return False

    async def get_hosts(self, connected_only: bool = True) -> Optional[NetworkHostsModel]:
        async with self._request('GET', '/network/hosts', params={'connectedOnly': 'true'} if connected_only else None) as response:
            if response.status == 200:
                json = await response.json()
                return NetworkHostsModel(**json)
            else:
                body = await response.text()
                _LOGGER.warning(f"failed to query for hosts (status code {response.status}): {body}")
                return None

    async def logout(self) -> bool:
        async with self._request('DELETE', f"/user/{self._token.userId}/token/{self._token.token}") as response:
            if response.status == 204:
                return True
            else:
                body = await response.text()
                _LOGGER.warning(f"failed to logout (status code {response.status}): {body}")
                return False

