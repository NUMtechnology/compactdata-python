def p_compactdata(p):
    """compactdata : top_level_map
    | value"""
    p[0] = p[1]


def p_top_level_map(p):
    """top_level_map : pair_list"""
    p[0] = dict(p[1])


def p_pair_list(p):
    """pair_list : pair SEMICOLON pair_list
    | pair"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_pair(p):
    """pair : key EQUALS value
    | key map
    | key array"""
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1], p[2])


def p_map(p):
    """map : LPAREN pair_list RPAREN"""
    p[0] = dict(p[2])


def p_array(p):
    """array : LBRACKET value_list RBRACKET"""
    p[0] = p[2]


def p_value_list(p):
    """value_list : array_value SEMICOLON value_list
    | array_value"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_array_value(p):
    """array_value : orphan_pair
    | value"""
    p[0] = p[1]


def p_orphan_pair(p):
    """orphan_pair : pair"""
    p[0] = dict([p[1]])


def p_value(p):
    """value : QUOTED_STRING
    | GRAVE_STRING
    | reserved
    | unquoted_value
    | map
    | array"""
    p[0] = p[1]


def p_reserved(p):
    """reserved : NULL
    | TRUE
    | FALSE"""
    if p[1] == "null":
        p[0] = None
    elif p[1] == "true":
        p[0] = True
    elif p[1] == "false":
        p[0] = False


# use type inference for unquoted values
def p_unquoted_value(p):
    """unquoted_value : UNQUOTED_VALUE"""
    try:
        p[0] = int(p[1])
    except ValueError:
        try:
            p[0] = float(p[1])
        except ValueError:
            p[0] = p[1]


def p_key(p):
    """key : UNQUOTED_VALUE
    | QUOTED_STRING
    | GRAVE_STRING"""
    p[0] = p[1]


# Error handling rule
def p_error(p):
    if p:
        raise Exception(f"Syntax error at token {p.type} ({p.value})")
    else:
        raise Exception("Syntax error at EOF")
