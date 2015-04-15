from parsers.baseparser import BaseParser
import re


class TVBParser(BaseParser):
    key = 'tvb'
    domains = ['news.tvb.com']
    page_prefix = 'http://news.tvb.com/'
    feeder_pattern = '^http://news.tvb.com/'
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
        # print (elt)
        self.title = elt.find('h4').contents[0]
        self.date = elt.find('span', 'time').getText()
        print('The title is: %s' % self.title)

        div = soup.find('div', id='c1_afterplayer').pre
        if div is None:
            self.real_article = False
            return

        self.body = '\n'.join(re.compile('\n+').split(div.getText().strip()))
        print('The body is: %s' % self.body)

    @classmethod
    def _get_all_page(cls, url):
        return [url]