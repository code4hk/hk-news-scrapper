from parsers.baseparser import BaseParser
import re


class AppleParser(BaseParser):
    code = 'apple'
    name = u'蘋果日報'
    domains = ['hk.apple.nextmedia.com']
    feeder_pattern = '^http://hk.apple.nextmedia.com/realtime/[a-z]+/[0-9]+/[0-9]+'
    feeder_pages = [
        'http://hk.apple.nextmedia.com/realtime/realtimelist/top',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/news',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/breaking',
        'http://hk.apple.nextmedia.com/enews/realtime/',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/china',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/international',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/finance',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/sports',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/magazine',
        'http://hk.apple.nextmedia.com/realtime/realtimelist/racing',
    ]

    def _parse(self, html):
        soup = self.soup(html)
        elt = soup.find('div', 'ArticleContent')
        if elt is None:
            self.real_article = False
            return
        self.body = '\n'.join(re.compile('\n+').split(elt.getText().strip()))
        self.title = soup.find('h1').getText().strip()
        date_elt = soup.find('span', 'last_update') or soup.find('span', 'pub_date')
        self.date = date_elt.getText()

    @classmethod
    def _get_all_page(cls, url):
        return [url]