from pydantic import BaseModel
from typing import Optional, List

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