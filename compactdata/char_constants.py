import re

infinity = float("inf")
reverse_solidus = f"\N{REVERSE SOLIDUS}"
quotation_mark = f"\N{QUOTATION MARK}"
grave_accent = f"\N{GRAVE ACCENT}"
backspace = f"\N{BACKSPACE}"
form_feed = f"\N{FORM FEED}"
line_feed = f"\N{LINE FEED}"
carriage_return = f"\N{CARRIAGE RETURN}"
tab = f"\N{HORIZONTAL TABULATION}"
tilde = f"\N{TILDE}"
left_parenthesis = f"\N{LEFT PARENTHESIS}"
right_parenthesis = f"\N{RIGHT PARENTHESIS}"
left_square_bracket = f"\N{LEFT SQUARE BRACKET}"
right_square_bracket = f"\N{RIGHT SQUARE BRACKET}"
semicolon = f"\N{SEMICOLON}"
equals_sign = f"\N{EQUALS SIGN}"
empty_string = ""

whitespace = backspace + form_feed + line_feed + carriage_return + tab

# Characters that require escaping in unquoted strings
unquoted_string_reserved_chars = (
    f"\\{left_parenthesis}"
    + f"\\{right_parenthesis}"
    + f"\\{left_square_bracket}"
    + f"\\{right_square_bracket}"
    + semicolon
    + equals_sign
)

quote_chars = [quotation_mark, grave_accent, empty_string]

escape_chars_regex = f"\\{reverse_solidus}{tilde}"  # reverse solidus has to be escaped
control_chars_regex = r"\x00-\x1f"  # control characters U+0000 to U+001F
unicode_escape_regex = r"u[0-9a-fA-F]{4}"
number_regex = re.compile(r"^(-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)$")
all_escaped_chars_regex = re.compile(f"[{escape_chars_regex}](.|{unicode_escape_regex})")

# A mapping of unescaped characters to their escaped equivalents
unescaped_to_escaped_map = {
    reverse_solidus: reverse_solidus,
    quotation_mark: quotation_mark,
    grave_accent: grave_accent,
    backspace: "b",
    form_feed: "f",
    line_feed: "n",
    carriage_return: "r",
    tab: "t",
    tilde: tilde,
    left_parenthesis: left_parenthesis,
    right_parenthesis: right_parenthesis,
    left_square_bracket: left_square_bracket,
    right_square_bracket: right_square_bracket,
    semicolon: semicolon,
    equals_sign: equals_sign,
}

for i in range(0x20):
    unescaped_to_escaped_map.setdefault(chr(i), "u{0:04x}".format(i))

escaped_to_unescaped_map = {v: k for k, v in unescaped_to_escaped_map.items()}

# The regexes are used to check if a string contains characters that need to be escaped
_chars_to_escape = {
    quotation_mark: re.compile(
        r"["
        f"{control_chars_regex}"
        f"{whitespace}"
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        r"]"  # comment to make black happy
    ),
    grave_accent: re.compile(
        r"["
        f"{control_chars_regex}"
        f"{whitespace}"
        f"{escape_chars_regex}"
        f"{grave_accent}"
        r"]"  # comment to make black happy
    ),
    empty_string: re.compile(
        r"["
        f"{control_chars_regex}"
        f"{whitespace}"
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        f"{grave_accent}"
        f"{unquoted_string_reserved_chars}"
        r"]"
    ),
}
_chars_to_escape_ascii = {
    quotation_mark: re.compile(
        r"(["
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
    grave_accent: re.compile(
        r"(["
        f"{escape_chars_regex}"
        f"{grave_accent}"
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
    empty_string: re.compile(
        r"(["
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        f"{grave_accent}"
        f"{unquoted_string_reserved_chars}"
        r"]|"
        r"[^ -~]"  # any character that is not between space U+0020 and tilde U+007E
        r")"
    ),
}

_chars_to_unescape = {
    quotation_mark: re.compile(
        f"(["
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        f"]|"
        f"{unicode_escape_regex}"
        f")"  # comment to make black happy
    ),
    grave_accent: re.compile(
        f"(["
        f"{escape_chars_regex}"
        f"{grave_accent}"
        f"]|"
        f"{unicode_escape_regex}"
        f")"  # comment to make black happy
    ),
    empty_string: re.compile(
        r"(["
        f"{escape_chars_regex}"
        f"{quotation_mark}"
        f"{grave_accent}"
        f"{unquoted_string_reserved_chars}"
        r"]|"
        f"{unicode_escape_regex}"
        r")"
    ),
}
