import aiohttp
from loguru import logger
from config import settings
from lxml import etree
import re
from urllib.parse import urlparse


class req_Mode_list(object):
    def __init__(self, modename, headers=None):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh;caicaizi) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        } if headers == None else headers
        self.proxy = None
        self.timeout = aiohttp.ClientTimeout(total=settings.Req_total, connect=settings.Req_connect,
                                             sock_connect=settings.Req_sock_connect, sock_read=settings.Req_sock_read)
        self.name = modename
        self.proxy = settings.request_proxy_pool if self.get_proxy(self.name) == True else None

    def get_proxy(self, module):
        """
        Get proxy
        :param str module: module name
        :return: proxy
        """
        if not settings.enable_request_proxy:
            logger.info('当前请求 {} 走不代理'.format(module))
            return False
        if settings.proxy_all_module:
            return False
        if module in settings.proxy_partial_module:
            logger.info('当前模块: {} 请求走代理'.format(module))
            return True

    def httpparser(self, url):
        if url.startswith(("http://", "https://")):
            data = urlparse(url)
            if data.path:
                url = url.replace(data.path, "/favicon.ico")
            else:
                url = url + "/favicon.ico"
            return url
        else:
            url = "http://" + url
            data = urlparse(url)
            if data.path:
                url = url.replace(data.path, "/favicon.ico")
            else:
                url = url + "/favicon.ico"
            return url

    async def get_url(self, url, headers=None):
        headers = self.headers if headers == None else headers
        async with aiohttp.ClientSession(headers=headers, timeout=self.timeout) as session:
            try:
                async with session.get(url=url, ssl=False, proxy=self.proxy) as resp:
                    if resp.status != 404:
                        return await resp.text()
                    else:
                        return None
            except Exception as e:
                logger.info("当前错误为{}".format(e))
                return None

    async def post_url(self, url, data):
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            try:
                async with session.post(url=url, ssl=False, data=data, proxy=self.proxy) as resp:
                    if resp.status != 404:
                        return await resp.text()
                    else:
                        return None
            except Exception as e:
                logger.info("当前错误为{}".format(e))
                return None

    async def post_json(self, url, data):
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            try:
                async with session.post(url=url, ssl=False, json=data, proxy=self.proxy) as resp:
                    if resp.status != 404:
                        return await resp.json()
                    else:
                        return None
            except Exception as e:
                logger.info("当前错误为{}".format(e))
                return None

    async def parser_xpath(self, html):
        try:
            if html:
                response = etree.HTML(html)
                return response
            else:
                logger.error("当前请求为空")
                return None
        except Exception as e:
            logger.error(e)

    async def listset(self, listdata, setlist):
        for ip in listdata:
            if r"\n" in ip:
                continue
            setlist.add(ip)
        return setlist

    async def rehtml(self, recode, html):
        try:
            if html:
                data = re.findall(recode, html)
                if data:
                    return data[0]
            else:
                return None
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    pass
