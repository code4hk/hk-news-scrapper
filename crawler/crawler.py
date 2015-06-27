from model.models import Articles
from parsers import get_parser
from parsers import parsers
from util import logger
import asyncio

log = logger.get(__name__)


def canonicalize_url(url):
    return url.split('?')[0].split('#')[0].strip()


def get_existing_urls(articles):
    return articles.get_all_active_urls(5)


@asyncio.coroutine
def crawl_all():
    articles = Articles()
    visited = set()
    coroutines = [parser.feed_urls() for parser in parsers]
    for coroutine in asyncio.as_completed(coroutines):
        urls = list(map(canonicalize_url, (yield from coroutine)))
        if len(urls) < 1:
            continue
        parser = get_parser(urls[0])
        log.info('Got {} URLs for {}'.format(len(urls), parser.domain))
        to_get = [parser(x).parse() for x in urls if x not in visited]
        visited = visited.union(urls)
        for get_page in asyncio.as_completed(to_get):
            try:
                page = yield from get_page
                articles.save_entry(page)
            except Exception as e:
                log.error(e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl_all())
    loop.close()


if __name__ == '__main__':
    main()