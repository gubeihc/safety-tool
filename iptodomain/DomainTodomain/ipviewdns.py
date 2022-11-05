import asyncio
from core import req_mode
from loguru import logger

class domain_url():
    def __init__(self):
        self.name = "ipviewdns"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()

    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://viewdns.info/reverseip/?host={ip}&t=1")
            xpath_html = await  self.mode.parser_xpath(html)
            namelist = xpath_html.xpath('//table/tr/td[1]/text()')
            result = await self.mode.listset(namelist[1:-16], self.urls)
            logger.success(f"ipviewdns get domain {len(result)}")
            return result
        except Exception as e:

            logger.error(e)


if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("110.242.68.66"))
