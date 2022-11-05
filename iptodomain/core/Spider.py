from .domain_plugin import spiderplus
from loguru import logger


class SpiderMain(object):
    def __init__(self, domain):
        self.root = domain
    async def crawl(self, ip):
        try:
            disallow = ["test"]
            _plugin = spiderplus("DomainTodomain", disallow)
            html = await  _plugin.work_domain(ip)
            result = [str(url).replace("/", "")for url in html]
            return result
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    pass
