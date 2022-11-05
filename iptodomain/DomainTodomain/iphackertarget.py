import asyncio
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        self.name = "iphackertarget"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()

    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://api.hackertarget.com/reverseiplookup/?q={ip}")
            if html:
                result = await self.mode.listset(html.split("\n"), self.urls)
                logger.success(f"iphackertarget get domain {len(result)}")
                return result
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("183.3.226.35"))
