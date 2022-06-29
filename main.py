import asyncio
import logging
import os
from multiprocessing import Pool

from cli import get_args_from_cli
from crawler import Crawler
from helpers import get_target_sites_from_file
from init_logging import init_logging


def run(*args):
    logging.info(*args)
    args = args[0]
    crawler = Crawler(*args)
    asyncio.run(crawler.run())


if __name__ == '__main__':
    init_logging()
    os.makedirs('results', exist_ok=True)
    args_ = get_args_from_cli()
    target_list = get_target_sites_from_file(file_path=args_.target_file)
    with Pool(processes=args_.cores_amount) as pool:
        pool.map(run, [(target_site, args_.links_limit, args_.depth_level) for target_site in target_list])
