from core.Spider import SpiderMain
import argparse
import asyncio
import os
from loguru import logger
import re

parser = argparse.ArgumentParser("ip查询域名-顾北")
parser.add_argument('-u', help='python3 main -u 110.242.68.3', metavar='')
parser.add_argument('-f', help='python3 main -f ip.txt 文件只支持 单个ip一行', metavar='')
args = parser.parse_args()


async def save(name, data):
    ##新建文件夹result 判断是否存在
    if not os.path.exists('result'):
        os.mkdir('result')
    try:
        nametext = "result/" + name + '.txt'
        with open(nametext, 'a') as f:
            for url in data:
                f.write(url + "\n")
        logger.info("文件保存到{}".format(nametext))
    except Exception as e:
        print(e)


# 创建ip反查询域名
async def get_domain_to_url(ip):
    # 通过正则匹配ip,错误ip
    try:
        if re.match(r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$', ip):
            # 通过正则过滤内网ip
            if re.match(r'^(10|127|172\.16|192\.168)\.', ip):
                logger.error("内网ip")
                return False
            logger.info("开始查询{}".format(ip))
            spider = SpiderMain(ip)
            result = await spider.crawl(ip)
            await save(ip, result)
        else:
            logger.error("ip格式错误")
    except Exception as e:
        logger.error(e)


async def main():
    if args.u and args.f:
        logger.error("参数错误 单个ip和文件只能选择一个")
    elif args.f:
        with open(args.f, 'r') as f:
            for i in f:
                await get_domain_to_url(i.strip())
    elif args.u:
        await get_domain_to_url(args.u)
    else:
        print('请输入参数')


if __name__ == '__main__':
    asyncio.run(main())
