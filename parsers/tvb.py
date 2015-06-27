from .baseparser import BaseParser
import asyncio
import re


class TVBParser(BaseParser):
    code = 'tvb'
    name = u'無綫新聞'
    domain = 'news.tvb.com'
    feeder_pattern = '^http://news.tvb.com/[a-z]+/[0-9]+[0-9a-zA-Z]+/'
    feeder_pages = [
        'http://news.tvb.com/list/focus/',
        'http://news.tvb.com/list/instant/',
        'http://news.tvb.com/list/local/',
        'http://news.tvb.com/list/greaterchina/',
        'http://news.tvb.com/list/world/',
        'http://news.tvb.com/list/finance/',
        'http://news.tvb.com/list/sports/',
        'http://news.tvb.com/list/parliament/'
    ]

    def _parse(self, html):
        soup = self.soup(html)
        elt = soup.find('div', 'newsDesc')
        if elt is None:
            self.real_article = False
            return

        title = elt.find('h4')
        if title is None:
            self.real_article = False
            return

        self.title = title.contents[0]
        self.date = elt.find('span', 'time').getText()

        div = soup.find('div', id='c1_afterplayer').pre
        if div is None:
            self.real_article = False
            return

        self.body = '\n'.join(re.compile('\n+').split(div.getText().strip()))

    @classmethod
    @asyncio.coroutine
    def _get_all_page(cls, url):
        return [url]