# SPDX-FileCopyrightText: 2024-present Miles Yucht <mgyucht@gmail.com>
#
# SPDX-License-Identifier: MIT
import asyncio
import logging
from .client import SagemcomF3896LGApi

logging.basicConfig(level=logging.DEBUG)


# Main entry to run the async function
async def main():
    with SagemcomF3896LGApi(password=input('Enter router password:')) as api:
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