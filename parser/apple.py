from parser.baseparser import BaseParser
import re


class AppleParser(BaseParser):
    domains = ['hk.apple.nextmedia.com']
    feeder_pattern = '^http://hk.apple.nextmedia.com/realtime/[a-z]+/[0-9]+/[0-9]+'
    feeder_pages = [
        'http://hk.apple.nextmedia.com/realtime/top/index',
        'http://hk.apple.nextmedia.com/realtime/news/index',
        'http://hk.apple.nextmedia.com/realtime/breaking/index',
        'http://hk.apple.nextmedia.com/realtime/enews/index',
        'http://hk.apple.nextmedia.com/realtime/finance/index',
        'http://hk.apple.nextmedia.com/realtime/china/index',
        'http://hk.apple.nextmedia.com/realtime/international/index',
        'http://hk.apple.nextmedia.com/realtime/sports/index',
        'http://hk.apple.nextmedia.com/realtime/magazine/index',
        'http://hk.apple.nextmedia.com/realtime/racing/index',
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
        # todo: load more pages
        return [url]