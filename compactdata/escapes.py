from compactdata.char_constants import (
    _chars_to_escape,
    _chars_to_escape_ascii,
    empty_string,
    infinity,
    number_regex,
    quotation_mark,
    quote_chars,
    reverse_solidus,
    unescaped_to_escaped_map,
)
from compactdata.exceptions import CompactDataEncodeError


def escape_replacer(escape_char, chars_to_escape):
    def replace(match):
        char = match.group(0)
        if char in unescaped_to_escaped_map:
            return escape_char + unescaped_to_escaped_map[char]
        else:
            return f"{escape_char}u{ord(char):04x}"

    return lambda s: chars_to_escape.sub(replace, s)


def encode_basestring(s, escape_char=None, quote_char=None, shortest=None, chars_to_escape=_chars_to_escape):
    if escape_char is None and quote_char is None and shortest is None:
        escape_char = reverse_solidus
        quote_char = quotation_mark
        shortest = True
    if escape_char is None:
        escape_char = reverse_solidus
    if quote_char is None:
        quote_char = quotation_mark

    leading_or_trailing_whitespace = s and (s[0] == " " or s[-1] == " ")
    # only_digits is true if whole string matches the regex number_regex
    only_digits = s and number_regex.fullmatch(s)

    if leading_or_trailing_whitespace and quote_char == empty_string:
        raise CompactDataEncodeError("Cannot encode string with leading or trailing whitespace as an unquoted string")
    if only_digits and quote_char == empty_string:
        raise CompactDataEncodeError("Cannot encode string with only digits as an unquoted string")

    if shortest:
        best_length = infinity
        best_result = None
        for quote_char in quote_chars:
            if quote_char == empty_string and (leading_or_trailing_whitespace or only_digits):
                continue
            char_escape_map = chars_to_escape[quote_char]
            replacer = escape_replacer(escape_char, char_escape_map)
            result = replacer(s)

            if quote_char:
                result = quote_char + result + quote_char

            if len(result) < best_length:
                best_length = len(result)
                best_result = result
        return best_result

    char_escape_map = chars_to_escape[quote_char]
    replacer = escape_replacer(escape_char, char_escape_map)
    result = replacer(s)

    if quote_char:
        return quote_char + result + quote_char
    else:
        return result


def encode_basestring_ascii(s, escape_char=reverse_solidus, quote_char=quotation_mark, shortest=True):
    return encode_basestring(s, escape_char, quote_char, shortest, chars_to_escape=_chars_to_escape_ascii)
