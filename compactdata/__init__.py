import logging

from compactdata.decoder import CompactDataDecodeError, create_parser, get_lexer_and_parser
from compactdata.encoder import CompactDataEncodeError, CompactDataEncoder

logger = logging.getLogger(__name__)

_default_encoder = CompactDataEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    default=None,
    sort_keys=False,
    escape_char="\\",
    quote_char='"',
)


def tokenize(compactdata_string: str, debug: bool = False) -> list[str]:
    lexer, _ = get_lexer_and_parser(debug)
    lexer.input(compactdata_string)
    token_list = list(lexer)
    return token_list


def loads(compactdata_string: str, debug: bool = False):
    _, parser = get_lexer_and_parser(debug)
    try:
        result = parser.parse(compactdata_string)
    except Exception as e:
        raise CompactDataDecodeError("Error decoding Compact Data string") from e
    return result


def dumps(
    obj,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    default=None,
    sort_keys=False,
    escape_char="\\",
    quote_char='"',
    shortest=True,
    dns_optimized=False,
):
    if (
        not skipkeys
        and ensure_ascii
        and check_circular
        and allow_nan
        and cls is None
        and indent is None
        and default is None
        and not sort_keys
        and escape_char == "\\"
        and quote_char == '"'
        and shortest
        and not dns_optimized
    ):
        # use cached encoder
        return _default_encoder.encode(obj)
    if cls is None:
        cls = CompactDataEncoder
    return cls(
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        default=default,
        sort_keys=sort_keys,
        escape_char=escape_char,
        quote_char=quote_char,
        shortest=shortest,
        dns_optimized=dns_optimized,
    ).encode(obj)


def load(fp, debug: bool = False):
    return loads(fp.read(), debug)


def dump(
    obj,
    fp,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    default=None,
    sort_keys=False,
    escape_char="\\",
    quote_char='"',
    shortest=True,
    dns_optimized=False,
):
    for chunk in dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        default=default,
        sort_keys=sort_keys,
        escape_char=escape_char,
        quote_char=quote_char,
        shortest=shortest,
        dns_optimized=dns_optimized,
    ):
        fp.write(chunk)
