import os
import sys
import asyncio
from loguru import logger


# 定义一个插件类 用来加载其他代码
class spiderplus(object):
    def __init__(self, plugin, disallow=None):
        self.dir_exploit = []
        self.disallow = ['__init__']
        self.disallow.extend(disallow)
        self.plugin = os.getcwd() + '/' + plugin
        self.urllist = []
        sys.path.append(self.plugin)

    def list_plusg(self):
        def filter_func(file):
            if not file.endswith(".py"):
                return False
            for disfile in self.disallow:
                if disfile in file:
                    return False
            return True

        dir_exploit = filter(filter_func, os.listdir(self.plugin))
        return list(dir_exploit)

        # 定义一个函数，用来循环去重复

    def remove_repeat(self, list):
        try:
            for i in list:
                if i not in self.urllist:
                    self.urllist.append(i)
        except Exception as e:
            pass

    async def work_domain(self, domain):
        result = []
        for _plugin in self.list_plusg():
            try:
                m = __import__(_plugin.split('.')[0])
                spider = getattr(m, 'domain_url')
                p = spider()
                s = asyncio.create_task(p.run(domain))
                result.append(s)
            except Exception as e:
                logger.error(e)
        logger.info("共执行插件{}个".format(len(result)))
        if result:
            # 去重复
            urls = await asyncio.wait(result)
            for url in urls:
                for u in url:
                    self.remove_repeat(u.result())
            return self.urllist
        else:
            logger.error("当前并没有插件加载")


if __name__ == '__main__':
    pass
