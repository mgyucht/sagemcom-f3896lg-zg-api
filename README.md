# sagemcom-f3896lg-zg-api

[![PyPI - Version](https://img.shields.io/pypi/v/sagemcom-f3896lg-zg-api.svg)](https://pypi.org/project/sagemcom-f3896lg-zg-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sagemcom-f3896lg-zg-api.svg)](https://pypi.org/project/sagemcom-f3896lg-zg-api)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Overview

`sagemcom-f3896lg-zg-api` is a async Python client that interacts with the Sagemcom 

## Installation

```console
pip install sagemcom-f3896lg-zg-api
```

## Example

```py
ROUTER_ENDPOINT = "192.168.100.1"
PASSWORD = "..."
async def main():
    async with SagemcomF3896LGApi(router_endpoint=ROUTER_ENDPOINT, password=PASSWORD) as api:
        if await api.login():
            print("Logged in! Fetching connected hosts...")
            hosts = await api.get_hosts()
            for host in hosts.hosts.hosts:
                print(host.model_dump_json(indent=4))
        else:
            print("Failed to login!")
```

## License

`sagemcom-f3896lg-zg-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
