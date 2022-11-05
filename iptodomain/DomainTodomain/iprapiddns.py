import asyncio
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        self.name = "rapiddns"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()

    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://rapiddns.io/s/{ip}")
            response = await self.mode.parser_xpath(html)
            namelist = response.xpath('//table[@id="table"]/tbody/tr/td/text()')
            result = await self.mode.listset(namelist, self.urls)
            logger.success(f"rapiddns get domain {len(result)}")
            return self.urls
        except Exception as e:

            logger.error(e)


if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("183.3.226.35"))
