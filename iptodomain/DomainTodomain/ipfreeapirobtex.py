import asyncio
import json
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        self.name = "ipfreeapirobtex"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()

    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://freeapi.robtex.com/ipquery/{ip}")
            data=json.loads(html)
            if data.get('pas'):
                namelist=data.get("pas")
                for url in namelist:
                    self.urls.add(url.get("o"))
            logger.success(f"ipfreeapirobtex get domain {len(self.urls)}")
            return self.urls
        except Exception as e:

            logger.error(e)


if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("183.3.226.35"))
