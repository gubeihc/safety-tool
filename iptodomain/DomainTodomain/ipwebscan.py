import asyncio
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        self.name = "ipwebscan"
        self.headers = {
            "origin": "https://www.webscan.cc",
            "referer": "https://www.webscan.cc/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        self.mode = req_mode.req_Mode_list(self.name, self.headers)
        self.urls = set()

    async def run(self, ip):
        try:
            data = {"domain": ip}
            html = await self.mode.post_url("https://www.webscan.cc/", data)
            if html:
                xpath_html = await  self.mode.parser_xpath(html)
                namelist = xpath_html.xpath('//div[@class="bd"]/ul//li/a[@class="domain"]/text()')
                result = await self.mode.listset(namelist, self.urls)
                logger.success(f"ipwebscan get domain {len(result)}")
                return result
            else:
                logger.info("ipwebscan not get domain")
        except  Exception as e:
            logger.error(e)


if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("110.242.68.66"))
