"""
Test a parser.  For example:
$ python parser/test_parser.py singtao.STParser http://std.stheadline.com/breakingnews/20150327a144036.asp
[text of article to store]
"""

import sys

try:
    parser_name = sys.argv[1]
except IndexError:
    print('Usage: test_parser.py <module_name>.<class_name> [<url_to_check>]')
    sys.exit()

try:
    url = sys.argv[2]
except IndexError:
    url = None

module, class_name = parser_name.rsplit('.', 1)
parser = getattr(__import__(module, globals(), fromlist=[class_name]), class_name)

if url:
    parsed_article = parser(url)
    print(str(parsed_article))
else:
    links = parser.feed_urls()
    print('\n'.join(links))
