"""
Test a parser.  For example:
$ python parsers/test_parser.py parsers.singtao.STParser http://std.stheadline.com/breakingnews/20150327a144036.asp
[text of article to store]
"""

import asyncio
import time
import sys

try:
    parser_name = sys.argv[1]
except IndexError:
    print('Usage: test_parser.py <package_name>.<module_name>.<class_name> [<url_to_check>]')
    sys.exit()

try:
    url = sys.argv[2]
except IndexError:
    url = None

package, module, class_name = parser_name.rsplit('.', 2)
parser = getattr(__import__(package+'.'+module, globals(), fromlist=[class_name]), class_name)


@asyncio.coroutine
def print_links():
    start_time = time.time()
    links = yield from parser.feed_urls()
    print('\n'.join(links))
    print("Time used: {}".format(time.time()-start_time))

if url:
    parsed_article = parser(url)
    print(str(parsed_article))
else:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_links())
