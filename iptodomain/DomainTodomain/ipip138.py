import asyncio
import json
from core import req_mode
from loguru import logger


class domain_url():
    def __init__(self):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "Hm_lvt_5eae533355dec90155c46ae3ec820c53=1666688349; Hm_lpvt_5eae533355dec90155c46ae3ec820c53=1666755992",
            "Referer": "https://site.ip138.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }
        self.name = "ip138"
        self.mode = req_mode.req_Mode_list(self.name, headers)
        self.urls = set()

    async def run(self, ip):
        page = 2
        try:
            html = await self.mode.get_url(f"https://site.ip138.com/{ip}/")
            if "502 Bad Gateway" in html:
                logger.info("ip138 502 Bad Gateway 当前ip被封了")
                return self.urls
            xpath_html = await  self.mode.parser_xpath(html)
            token = await self.mode.rehtml("var _TOKEN = '(.*)';", html)
            namelist = xpath_html.xpath('//div[@class="result result2"]/ul/li/a/@href')
            result = await self.mode.listset(namelist, self.urls)
            while True:
                url = f"https://site.ip138.com/index/querybyip/?ip={ip}&page={page}&token={token}"
                page += 1
                html = await self.mode.get_url(url)
                if html:
                    if "502 Bad Gateway" in html:
                        logger.info("ip138 502 Bad Gateway 当前ip被封了")
                        return self.urls
                    try:
                        json_html = json.loads(html)
                        if json_html.get("data"):
                            for i in json_html['data']:
                                s = i['domain'].replace("/", "")
                                self.urls.add(s)
                        else:
                            break
                    except Exception as e:
                        print(e)
            logger.success(f"ip138 get domain {len(self.urls)}")
            return result
        except Exception as e:
            logger.error(e)
if __name__ == '__main__':
    data = domain_url()
    asyncio.run(data.run("110.242.68.4"))
