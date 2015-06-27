from bs4 import BeautifulSoup
from util import logger
import asyncio
import aiohttp
import re


log = logger.get(__name__)


@asyncio.coroutine
def grab_url(url, max_retry=5):
    text = None
    retry = False
    try:
        # todo:
        # TimeoutError: [Errno 60] Operation timed out
        # Fatal read error on socket transport
        response = yield from aiohttp.request('GET', url)
        text = yield from response.read()
        assert response.status == 200
    except (AssertionError, aiohttp.ClientOSError, aiohttp.ClientResponseError):
        yield from asyncio.sleep(6-max_retry)
        retry = True
    if retry:
        if max_retry == 0:
            raise RuntimeError('Too many attempts to download %s' % url)
        return (yield from grab_url(url, max_retry - 1))
    log.debug('Retrieved %s', url)
    return text


class BaseParser(object):
    code = None
    name = None
    domain = None
    feeder_pattern = ''
    feeder_pages = []  # index page for news
    date = None
    title = None
    body = None
    lang = 'zh_Hant'
    encoding = 'utf-8'

    real_article = True  # If set to False, ignore this article

    def __init__(self, url):
        self.url = url

    @asyncio.coroutine
    def parse(self):
        html = yield from grab_url(self.url)
        self._parse(html)
        return self

    def _parse(self, html):
        """Should take html and populate self.(date, title, byline, body)
        If the article isn't valid, set self.real_article to False and return.
        """
        raise NotImplementedError()

    def __str__(self):
        return u'\n'.join((self.date, self.title, self.body,))

    @classmethod
    def soup(cls, html):
        return BeautifulSoup(html, from_encoding=cls.encoding)

    @classmethod
    @asyncio.coroutine
    def _get_all_page(cls, url):
        """Take the article list url and return a list of urls corresponding to all pages
        """
        raise NotImplementedError()

    @classmethod
    @asyncio.coroutine
    def feed_urls(cls):
        all_urls = []
        coroutines = [cls._get_all_page(feeder_url) for feeder_url in cls.feeder_pages]
        for coroutine in asyncio.as_completed(coroutines):
            for page in (yield from coroutine):
                try:
                    source = yield from grab_url(page)
                    urls = [a.get('href') or '' for a in cls.soup(source).findAll('a')]
                    urls = [url if '://' in url else "http://{}{}".format(cls.domain, url) for url in urls]
                    all_urls += [url for url in urls if re.search(cls.feeder_pattern, url)]
                except RuntimeError:
                    log.info("Can't load page {}.  skipping...".format(page))
        return all_urls