from operator import concat
from bs4 import BeautifulSoup
from util import logger
import urllib.request
import urllib.error
import http.cookiejar
import socket
import time
import re


log = logger.get(__name__)


def grab_url(url, max_retry=5, opener=None):
    text = None
    if opener is None:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    retry = False
    try:
        text = opener.open(url, timeout=5).read()
    except (socket.timeout, urllib.error.URLError):
        retry = True
    if retry:
        if max_retry == 0:
            raise Exception('Too many attempts to download %s' % url)
        time.sleep(0.5)
        return grab_url(url, max_retry - 1, opener)
    log.debug('Retrieved %s', url)
    return text


class BaseParser(object):
    key = None
    domains = []
    # These should be filled in by self._parse(html)
    page_prefix = ''
    feeder_pattern = ''
    feeder_pages = []  # index page for news
    date = None
    title = None
    body = None
    encoding = 'big5hkscs'

    real_article = True  # If set to False, ignore this article

    def __init__(self, url):
        try:
            self.html = grab_url(url)
        except urllib.request.HTTPError as e:
            if e.code == 404:
                self.real_article = False
                return
            raise
        self._parse(self.html)

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
    def _get_all_page(cls, url):
        """Take the article list url and return a list of urls corresponding to all pages
        """
        raise NotImplementedError()

    @classmethod
    def feed_urls(cls):
        all_urls = []
        for feeder_url in cls.feeder_pages:
            domain = '/'.join(feeder_url.split('/')[:3])
            for page in cls._get_all_page(feeder_url):
                urls = [a.get('href') or '' for a in cls.soup(grab_url(page)).findAll('a')]
                urls = [url if '://' in url else concat(domain, url) for url in urls]
                all_urls += [url for url in urls if re.search(cls.feeder_pattern, url)]
        return all_urls