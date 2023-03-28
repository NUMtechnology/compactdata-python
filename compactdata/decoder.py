import logging

from compactdata.grammar_rules import *  # noqa
from compactdata.token_definitions import *  # noqa
from ply import lex as lex
from ply import yacc as yacc

logger = logging.getLogger(__name__)


class CompactDataDecodeError(Exception):
    pass


def create_parser(debug: bool = False):
    lexer = lex.lex(debug=debug, debuglog=logger)
    parser = yacc.yacc(debug=debug, debuglog=logger)
    return lexer, parser


_lexer, _parser = create_parser(debug=False)
_debug_lexer, _debug_parser = create_parser(debug=True)


def get_lexer_and_parser(debug: bool = False):
    if debug:
        return _debug_lexer, _debug_parser
    return _lexer, _parser
