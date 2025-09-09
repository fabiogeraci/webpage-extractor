import httpx
from ...domain.ports import HttpClientPort


class HttpxClient(HttpClientPort):
    def __init__(self):
        self._client = httpx.AsyncClient(follow_redirects=True, headers={
        "User-Agent": "webpage-extractor/0.1 (+https://example.com)"
        })


    async def get_text(self, url: str, timeout: float = 20.0) -> str:
        resp = await self._client.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text


    async def get_bytes(self, url: str, timeout: float = 20.0) -> bytes:
        resp = await self._client.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.content