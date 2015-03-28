# http://std.stheadline.com/breakingnews/20150327a144036.asp

from operator import concat
from baseparser import BaseParser
from baseparser import grab_url
import re


class STParser(BaseParser):
    page_prefix = 'http://std.stheadline.com/breakingnews/'
    feeder_pattern = '^http://std.stheadline.com/breakingnews/'
    feeder_pages = [
        'http://std.stheadline.com/breakingnews/instantnews_locfrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_intfrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_chifrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_finfrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_profrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_spofrontpage.html',
        'http://std.stheadline.com/breakingnews/instantnews_entfrontpage.html',
    ]

    def _parse(self, html):
        soup = self.soup(html)
        elt = soup.find('div', 'heading')
        if elt is None:
            self.real_article = False
            return
        self.title = elt.find('h1').getText()
        self.date = elt.find('span').getText()

        div = soup.find('div', 'content')
        if div is None:
            self.real_article = False
            return
        self.body = '\n'.join(re.compile('\n+').split(div.getText().strip()))

    @classmethod
    def _get_all_page(cls, url):
        soup = cls.soup(grab_url(url))
        urls = [url]
        urls += [concat(cls.page_prefix, link.get('href')) for link in soup.find_all('a', 'papernewstop')[:-1]]
        return urls