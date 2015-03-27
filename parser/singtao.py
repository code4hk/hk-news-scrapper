# http://std.stheadline.com/breakingnews/20150327a144036.asp

from bs4 import BeautifulSoup

from baseparser import BaseParser


class STParser(BaseParser):
    def _parse(self, html):
        soup = BeautifulSoup(html, from_encoding='big5')

        self.meta = soup.findAll('meta')
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
        self.body = div.getText().strip()
