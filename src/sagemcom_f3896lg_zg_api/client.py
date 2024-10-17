from typing import List, Optional
import aiohttp
import logging
from multidict import CIMultiDict
from pydantic import BaseModel

_LOGGER = logging.getLogger(__name__)

API_BASE = "/rest/v1"

class TokenModel(BaseModel):
    token: str
    userLevel: str
    userId: int

class LoginResponseModel(BaseModel):
    created: TokenModel

# Model for Ethernet configuration
class EthernetModel(BaseModel):
    port: int

# Model for IPv4 configuration
class IPv4Model(BaseModel):
    address: str
    leaseTimeRemaining: int

# Model for IPv6 configuration
class IPv6Model(BaseModel):
    linkLocalAddress: str
    globalAddress: str
    leaseTimeRemaining: int

# Model for the device configuration
class ConfigModel(BaseModel):
    connected: bool
    deviceName: str
    deviceType: str
    hostname: str
    interface: str
    speed: int
    ethernet: EthernetModel
    ipv4: IPv4Model
    ipv6: Optional[IPv6Model] = None  # IPv6 may not always be present

# Model for each host (device)
class HostModel(BaseModel):
    macAddress: str
    config: ConfigModel

# Model for the hosts key
class HostsModel(BaseModel):
    hosts: List[HostModel]

# Top-level model for the JSON
class NetworkHostsModel(BaseModel):
    hosts: HostsModel

class SagemcomF3896LGApi:
    def __init__(self, password: str, router_endpoint: str = '192.168.178.1') -> None:
        self._password = password
        self._router_endpoint = router_endpoint
        self._session = None

    async def close(self):
        if self._session is not None:
            await self.logout()
            await self._session.close()

    def __aenter__(self) -> 'SagemcomF3896LGApi':
        return self

    def __aexit__(self) -> None:
        self.close()

    def _get_api_base(self) -> str:
        return f"http://{self._router_endpoint}{API_BASE}"

    def get_headers(self) -> CIMultiDict[str]:
        return self._session.headers

    async def login(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._get_api_base()}/user/login", json={'password': self._password}) as response:
                if response.status == 201:
                    json = await response.json()
                    data = LoginResponseModel(**json)
                    self._session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {data.created.token}'})
                    return True
                else:
                    body = await response.text()
                    _LOGGER.warning(f"failed to login (status code {response.status}): {body}")
                    return False

    async def get_hosts(self, connected_only: bool = True) -> Optional[NetworkHostsModel]:
        endpoint = f"{self._get_api_base()}/network/hosts"
        if connected_only:
            endpoint += "?connectedOnly=true"
        async with self._session.get(endpoint) as response:
            if response.status == 200:
                json = await response.json()
                return NetworkHostsModel(**json)
            else:
                body = await response.text()
                _LOGGER.warning(f"failed to query for hosts (status code {response.status}): {body}")
                return None

    async def logout(self) -> None:
        pass

