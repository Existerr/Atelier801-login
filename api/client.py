import aiohttp

from random import choice

class Client(aiohttp.ClientSession):
    
    def __init__(self, agents=None, proxy=None):
        super().__init__(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        })

        self.agents = agents
        self.proxy = proxy

    async def request(self, method, url, **kwargs):
        return_object = kwargs.pop("return_object", False)

        headers = kwargs.pop("headers", {})
        if self.agents:
            headers["User-Agent"] = choice(self.agents)

        try:
            async with super().request(method, url, proxy=self.proxy, headers=headers, **kwargs) as response:
                data = {
                    "text": await response.text(),
                    "cookies": { key: cookie.value for key, cookie in response.cookies.items() }
                } if return_object else await response.json(content_type="text/html")

        except Exception:
            data = None

        return data
