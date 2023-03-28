import re

INFINITY = float("inf")

ESCAPE_DCT = {
    "\\": "\\",  # reverse solidus U+005C
    '"': '"',  # quotation mark       U+0022
    "`": "`",  # grave accent         U+0060
    "\b": "b",  # backspace           U+0008
    "\f": "f",  # form feed           U+000C
    "\n": "n",  # line feed           U+000A
    "\r": "r",  # carriage return     U+000D
    "\t": "t",  # tab                 U+0009
    "~": "~",  # tilde                U+007E
    "(": "(",  # left parenthesis     U+0028
    ")": ")",  # right parenthesis    U+0029
    "[": "[",  # left square bracket  U+005B
    "]": "]",  # right square bracket U+005D
    ";": ";",  # semicolon            U+003B
    "=": "=",  # equals sign          U+003D
}
for i in range(0x20):
    ESCAPE_DCT.setdefault(chr(i), "u{0:04x}".format(i))

ESCAPE_REGEX_DICT = {
    "`": re.compile(
        r"["
        r"\x00-\x1f"  # control characters U+0000 to U+001F
        r"\b"  # backspace           U+0008
        r"\f"  # form feed           U+000C
        r"\n"  # line feed           U+000A
        r"\r"  # carriage return     U+000D
        r"\t"  # horizontal tab      U+0009
        r"\\"  # reverse solidus     U+005C
        r"~"  # tilde                U+007E
        r"`"  # grave accent         U+0060
        r"]"
    ),
    '"': re.compile(
        r"["
        r"\x00-\x1f"  # control characters U+0000 to U+001F
        r"\b"  # backspace           U+0008
        r"\f"  # form feed           U+000C
        r"\n"  # line feed           U+000A
        r"\r"  # carriage return     U+000D
        r"\t"  # horizontal tab      U+0009
        r"\\"  # reverse solidus     U+005C
        r"~"  # tilde                U+007E
        r"\""  # quotation mark      U+0022
        r"]"
    ),
    "": re.compile(
        r"["
        r"\x00-\x1f"  # control characters U+0000 to U+001F
        r"\b"  # backspace            U+0008
        r"\f"  # form feed            U+000C
        r"\n"  # line feed            U+000A
        r"\r"  # carriage return      U+000D
        r"\t"  # horizontal tab       U+0009
        r"\\"  # reverse solidus      U+005C
        r"~"  # tilde                 U+007E
        r"\""  # quotation mark       U+0022
        r"`"  # grave accent          U+0060
        r"("  # left parenthesis      U+0028
        r")"  # right parenthesis     U+0029
        r"\["  # left square bracket  U+005B
        r"\]"  # right square bracket U+005D
        r";"  # semicolon             U+003B
        r"="  # equals sign           U+003D
        r"]"
    ),
}

ESCAPE_ASCII_REGEX_DICT = {
    "`": re.compile(
        r"(["
        r"\\"  # reverse solidus     U+005C
        r"~"  # tilde                U+007E
        r"`"  # grave accent         U+0060
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
    '"': re.compile(
        r"(["
        r"\\"  # reverse solidus     U+005C
        r"~"  # tilde                U+007E
        r"\""  # quotation mark      U+0022
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
    "": re.compile(
        r"(["
        r"\\"  # reverse solidus      U+005C
        r"~"  # tilde                 U+007E
        r"\""  # quotation mark       U+0022
        r"`"  # grave accent          U+0060
        r"("  # left parenthesis      U+0028
        r")"  # right parenthesis     U+0029
        r"\["  # left square bracket  U+005B
        r"\]"  # right square bracket U+005D
        r";"  # semicolon             U+003B
        r"="  # equals sign           U+003D
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
}


def escape_replacer(quote_char, escape_char, regex_dict):
    regex = regex_dict[quote_char]

    def replace(match):
        char = match.group(0)
        if char in ESCAPE_DCT:
            return escape_char + ESCAPE_DCT[char]
        else:
            return f"{escape_char}u{ord(char):04x}"

    return lambda s: regex.sub(replace, s)


def encode_basestring(s, escape_char="\\", quote_char='"', shortest=True, force_ascii=False):
    regex_dict = ESCAPE_ASCII_REGEX_DICT if force_ascii else ESCAPE_REGEX_DICT

    if shortest:
        best_length = INFINITY
        best_result = None
        for quote_char in regex_dict.keys():
            replacer = escape_replacer(quote_char, escape_char, regex_dict)
            result = replacer(s)

            if quote_char:
                result = quote_char + result + quote_char

            if len(result) < best_length:
                best_length = len(result)
                best_result = result
        return best_result

    replacer = escape_replacer(quote_char, escape_char, regex_dict)
    result = replacer(s)

    if quote_char:
        return quote_char + result + quote_char
    else:
        return result


def encode_basestring_ascii(s, escape_char="\\", quote_char='"', shortest=True):
    return encode_basestring(s, escape_char, quote_char, shortest, force_ascii=True)
