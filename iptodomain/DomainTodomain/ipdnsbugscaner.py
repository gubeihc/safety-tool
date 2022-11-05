import asyncio
from core import req_mode
from loguru import logger
class domain_url():
    def __init__(self):
        self.name = "ipdnswebscaner"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()
    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"http://dns.bugscaner.com/{ip}.html")
            xpath_html = await  self.mode.parser_xpath(html)
            namelist = xpath_html.xpath('//table[@class="table table-bordered"]/tbody/tr/td/a/text()')
            result = await self.mode.listset(namelist, self.urls)
            logger.success(f"ipdnswebscaner get domain {len(result)}")
            return result
        except Exception as e:
            logger.error(e)
if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("110.242.68.66"))
