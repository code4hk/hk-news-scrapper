import importlib

parsers = """
singtao.STParser
apple.AppleParser
tvb.TVBParser
""".split()

parser_dict = {}

# Import the parser and fill in parser_dict: domain -> parser
for parser_name in parsers:
    module, class_name = parser_name.rsplit('.', 1)
    parser = getattr(importlib.import_module('parsers.' + module), class_name)
    for domain in parser.domains:
        parser_dict[domain] = parser


def get_parser(url):
    return parser_dict[url.split('/')[2]]

# Each feeder places URLs into the database to be checked periodically.
parsers = [parser for parser in parser_dict.values()]

__all__ = ['parsers', 'get_parser']