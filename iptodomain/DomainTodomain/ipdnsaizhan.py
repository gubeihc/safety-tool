import asyncio
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        self.name = "ipdnsaizhan"
        self.headers = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "PHPSESSID=9pgsoocphln0n9q1pat216ioa7",
            "Referer": "https://dns.aizhan.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close"
        }
        self.mode = req_mode.req_Mode_list(self.name, self.headers)
        self.urls = set()

    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://dns.aizhan.com/{ip}/")
            xpath_html = await  self.mode.parser_xpath(html)
            namelist = xpath_html.xpath('//tbody//tr/td/a/text()')
            result = await self.mode.listset(namelist, self.urls)
            logger.success(f"ipdnsaizhan get domain {len(result)}")
            return self.urls
        except Exception as e:
            logger.error(e)
if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("183.3.226.35"))
