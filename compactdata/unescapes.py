from compactdata.char_constants import (
    _chars_to_unescape,
    all_escaped_chars_regex,
    escaped_to_unescaped_map,
    number_regex,
)
from compactdata.exceptions import CompactDataDecodeError


def unescape_replace(chars_to_unescape):
    def replace(match):
        char = match.group(1)
        if chars_to_unescape.match(char):
            return escaped_to_unescaped_map[char]
        elif char.startswith("u"):
            return chr(int(char[1:], 16))
        elif char.startswith("U"):
            return chr(int(char[1:], 16))
        else:
            raise CompactDataDecodeError(f"Invalid escape sequence: {match.group(0)}")

    return replace


def decode_string(s, quote_char):
    replacer = unescape_replace(_chars_to_unescape[quote_char])
    unescaped_string = all_escaped_chars_regex.sub(replacer, s)

    # Check if the string matches the number definition
    match = number_regex.fullmatch(unescaped_string)

    if match:
        number = match.group(1)
        if "." in number or "e" in number.lower():
            return float(number)
        else:
            return int(number)
    else:
        return unescaped_string
