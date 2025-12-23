import asyncio

import httpx


async def fetch(client: httpx.AsyncClient, url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        r = await client.get(url)
        r.raise_for_status()
        return r.text
