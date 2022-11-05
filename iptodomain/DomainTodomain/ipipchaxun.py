import asyncio
import json
from core import req_mode
from loguru import logger
class domain_url():
    def __init__(self):
        self.name = "ipipchaxun"
        self.mode = req_mode.req_Mode_list(self.name)
        self.urls = set()
    async def run(self, ip):
        try:
            html = await self.mode.get_url(f"https://ipchaxun.com/{ip}/")
            if html:
                xpath_html=await self.mode.parser_xpath(html)
                namelist=xpath_html.xpath('//div[@id="J_domain"]/p/a/text()')
                token = await self.mode.rehtml("_TOKEN = '(.*)';",html)
                page=2
                while 1:
                    next_html = await self.mode.get_url(f"https://ipchaxun.com/index/index/querybyip/?ip={ip}&page={page}&token={token}")
                    page = page +1
                    response = json.loads(next_html)
                    if len(response.get("data")) >1:
                        for url in response.get("data"):
                            self.urls.add(url.get("domain"))
                    else:
                        break
                await self.mode.listset(namelist, self.urls)
                logger.success(f"ipipchaxun get domain {len(self.urls)}")
                return self.urls
            else:
                logger.info(f"ipipchaxun get domain {len(self.urls)}")
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    data=domain_url()
    asyncio.run(data.run("110.242.68.66"))