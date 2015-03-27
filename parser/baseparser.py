import urllib.request
import http.cookiejar
import socket
import time


def grab_url(url, max_depth=5, opener=None):
    if opener is None:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    retry = False
    try:
        text = opener.open(url, timeout=5).read()
    except socket.timeout:
        retry = True
    if retry:
        if max_depth == 0:
            raise Exception('Too many attempts to download %s' % url)
        time.sleep(0.5)
        return grab_url(url, max_depth - 1, opener)
    return text


class BaseParser(object):
    # These should be filled in by self._parse(html)
    date = None
    title = None
    body = None

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