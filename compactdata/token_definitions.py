reserved = {
    "null": "NULL",
    "true": "TRUE",
    "false": "FALSE",
}

# Define the tokens
tokens = [
    "QUOTED_STRING",
    "GRAVE_STRING",
    "UNQUOTED_VALUE",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "EQUALS",
    "SEMICOLON",
] + list(reserved.values())

# Define the regular expressions for each token
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_EQUALS = r"="
t_SEMICOLON = r";"

# Ignore whitespace characters
t_ignore = " \t\n"


def t_GRAVE_STRING(t):
    r"`(?:[\\~][\\~`/bfnrt]|[\\~]u[0-9a-fA-F]{4}|[^\\`~])*`"
    t.value = t.value[1:-1]  # Remove backticks from value
    return t


def t_QUOTED_STRING(t):
    r'"(?:[\\~][\\~"/bfnrt]|[\\~]u[0-9a-fA-F]{4}|[^\\"~])*"'
    t.value = t.value[1:-1]  # Remove quotes from value
    return t


def t_UNQUOTED_VALUE(t):
    r'(?:[\\~][\\~`"/bfnrt\[\]\(\);=]|\\u[0-9a-fA-F]{4}|[^\\`"~\[\]\(\);=])+'
    t.type = reserved.get(t.value, "UNQUOTED_VALUE")
    return t


# Error handling rule
def t_error(t):
    raise Exception(f"Invalid character: {t.value[0]}")
    # t.lexer.skip(1)
