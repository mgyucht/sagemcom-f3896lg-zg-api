# SPDX-FileCopyrightText: 2024-present Miles Yucht <mgyucht@gmail.com>
#
# SPDX-License-Identifier: MIT
import asyncio
import getpass
import logging
from .client import SagemcomF3896LGApi

logging.basicConfig(level=logging.DEBUG)


# Main entry to run the async function
async def main():
    router_endpoint = input('Enter router IP: ')
    if not router_endpoint:
        print('No router specified, exiting')
    password = getpass.getpass('Enter router password: ')
    if not password:
        print('No password specified, exiting')
    async with SagemcomF3896LGApi(router_endpoint=router_endpoint, password=password) as api:
        if await api.login():
            print("Logged in! Fetching connected hosts...")
            hosts = await api.get_hosts()
            for host in hosts.hosts.hosts:
                print(host.model_dump_json(indent=4))
        else:
            print("Failed to login!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())