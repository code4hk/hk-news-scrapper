from model.models import Articles
from parsers import get_parser
from parsers import parsers
from util import logger
import urllib.request
import traceback

log = logger.get(__name__)


def canonicalize_url(url):
    return url.split('?')[0].split('#')[0].strip()


def get_all_new_article_urls():
    ans = set()
    for parser in parsers:
        log.info('Looking up %s' % parser.domains)
        urls = parser.feed_urls()
        ans = ans.union(map(canonicalize_url, urls))
        log.debug('Got %s urls so far' % len(ans))
    return ans


def get_existing_urls(articles):
    return articles.get_all_urls_older_than(20)


def get_all_article_urls(articles):
    return get_all_new_article_urls().union(get_existing_urls(articles))


def load_article(url):
    try:
        parser = get_parser(url)
    except KeyError:
        log.info('Unable to parse domain, skipping')
        return
    try:
        parsed_article = parser(url)
    except (AttributeError, urllib.request.HTTPError, Exception) as e:
        if isinstance(e, urllib.request.HTTPError) and e.msg == 'Gone':
            return
        log.error('Exception when parsing %s', url)
        log.error(traceback.format_exc())
        log.error('Continuing')
        return
    if not parsed_article.real_article:
        return
    return parsed_article


def update_articles():
    articles = Articles()
    all_urls = get_all_article_urls(articles)
    log.info('Got all %s urls; storing to database' % len(all_urls))
    for i, url in enumerate(all_urls):
        log.debug('Woo: %d/%d is %s' % (i+1, len(all_urls), url))
        parsed_article = load_article(url)
        if parsed_article is None:
            continue
        articles.save_revision(url, parsed_article.date, parsed_article.title, parsed_article.body)


def main():
    update_articles()
    pass

if __name__ == '__main__':
    main()