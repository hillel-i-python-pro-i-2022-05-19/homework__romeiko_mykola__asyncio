import asyncio

from crawler import Crawler
from init_logging import init_logging

crawler = Crawler()

if __name__ == '__main__':
    init_logging()
    asyncio.run(crawler.run())
