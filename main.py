from util.env import log_dir
from crawler import crawler
from daemon import Daemon
import sys


class CrawlerDaemon(Daemon):
    def run(self):

        while True:
            crawler.main()


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