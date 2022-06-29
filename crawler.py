import asyncio
import logging
import urllib

import aiohttp
import bs4

from custom_typing import *


class Crawler:
    def __init__(self, target_url: str = 'https://nba.com', links_limit: int = 100, depth_level: int = 2):
        self.target_url: T_URL = target_url
        self.target_urls: T_URLS = []
        self.links_limit = links_limit
        self.depth_level = depth_level
        self.current_depth_level: int = 1
        self.domain: T_DOMAIN | None = None
        self._aiohttp_session: aiohttp.ClientSession | None = None

    def create_aiohttp_session(self) -> None:
        self._aiohttp_session = aiohttp.ClientSession()

    def get_urls(self, text: T_HTML_TEXT, added_urls: int = 0) -> T_URLS:
        soup = bs4.BeautifulSoup(markup=text, features='html.parser')
        urls = []
        for link_element in soup.find_all('a'):
            url = link_element.get('href')
            if not self.is_url(url=url):
                continue
            if self.depth_level > 1 and self.current_depth_level <= self.depth_level and self.check_that_url_links_to_base_domain(url=url):
                self.target_urls.append(url)
                logging.info(msg=f'{url} - target url added.')
            logging.info(msg=f'{url} - url is added to results.')
            urls.append(url)
            if added_urls and len(urls) > self.links_limit - added_urls:
                break
            elif not added_urls and len(urls) > self.links_limit:
                break
        self.target_urls = list(set(self.target_urls))
        return urls

    async def get_text_from_url(self, url: T_URL = None) -> T_HTML_TEXT:
        async with self._aiohttp_session.get(url or self.target_url) as response:
            return await response.text()

    async def get_text_from_urls(self, target_urls: T_URLS) -> T_HTML_TEXTS:
        event_loop = asyncio.get_event_loop()
        tasks = [
            event_loop.create_task(self.get_text_from_url(url=url)) for url in target_urls
        ]
        result = await asyncio.gather(*tasks)
        return [html_text for html_text in result]

    def check_that_url_links_to_base_domain(self, url: T_URL) -> bool:
        domain = self.get_domain(url=url)
        if not self.domain:
            self.get_domain()
        return self.domain in domain

    def get_domain(self, url: T_URL = None) -> T_DOMAIN:
        parse_url_response = urllib.parse.urlsplit(url=(url or self.target_url))
        if not url:
            self.domain = parse_url_response[1]
        return parse_url_response[1]

    @staticmethod
    def is_url(url: T_URL) -> bool:
        parse_url_response = urllib.parse.urlsplit(url=url)
        if parse_url_response[0] in ('http', 'https'):
            return True
        return False

    def write_urls_to_the_file(self, urls: T_URLS):
        parse_url_response = urllib.parse.urlsplit(url=self.target_url)
        file_name = f'results/urls_list_from_{parse_url_response[1].replace(".","_")}.csv'
        with open(file_name, 'w') as file:
            urls = list(set(urls))
            file.write(','.join(urls))
            logging.info(msg=f'{file_name} was written to the disk(current directory).')

    async def run(self):
        result_urls = []
        try:
            self.create_aiohttp_session()
            result_urls = self.get_urls(await self.get_text_from_url())
            while self.current_depth_level < self.depth_level and len(result_urls) < self.links_limit:
                self.current_depth_level += 1
                html_text_from_urls = await self.get_text_from_urls(self.target_urls)
                for html_text in html_text_from_urls:
                    result_urls.extend(self.get_urls(text=html_text, added_urls=len(result_urls)))
            await self._aiohttp_session.close()
        except Exception as e:
            logging.exception(e)
        finally:
            self.write_urls_to_the_file(urls=result_urls)
            return result_urls
