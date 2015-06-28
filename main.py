from util.env import log_dir
from crawler import crawler
from daemon import Daemon
from util import logger
import asyncio
import sys


log = logger.get(__name__)


class CrawlerDaemon(Daemon):
    def run(self):
        loop = asyncio.get_event_loop()
        try:
            while True:
                log.info("crawler.main")
                crawler.main(loop)
        finally:
            loop.close()


if __name__ == '__main__':
    daemon = CrawlerDaemon(log_dir() + '/newsdiff_crawler.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)