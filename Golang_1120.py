import ply.lex as lex
import ply.yacc as yacc

# keywords
reserved = {
    'var': 'KVAR',
    'int': 'KINT',
    'bool': 'KBOOL',
}

# tokens
tokens = (
             'LOR', 'LAND',  # logical
             'LE', 'LT', 'GE', 'GT', 'EQ', 'NE',  # relational

             'ID', 'INT', 'BOOL'  # identifier
         ) + tuple(reserved.values())

t_LOR = r'\|\|'
t_LAND = r'&&'

t_LE = r'<='
t_LT = r'<'
t_GE = r'>'
t_GT = r'>='
t_EQ = r'=='
t_NE = r'!='


def t_BOOL(t):
    r'false|true'
    t.value = True if t.value == 'true' else False
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # keyword check
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


literals = [
    '=', '+', '-', '*', '/',  # arithmetic(except '=')
    '(', ')',  # parenthesis
    '!'  # logical
]

# Ignored characters
t_ignore = ' \t'


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


lex.lex()

# lexer.input("1+2+345")
# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)


# Parsing rules

precedence = (
    ('left', 'LAND', 'LOR'),
    ('right', '!'),

    ('nonassoc', 'LE', 'LT', 'GE', 'GT'),  # do not allow expanding
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS')
)

names = {}


def p_statement_var_assign(p):
    """statement : KVAR ID type "=" expression"""

    if p[3] == 'bool' and type(p[5]) != bool:
        print("TypeError: non bool type assigned to bool")
        names[p[2]] = False

    elif p[3] == 'int' and type(p[5]) != int:
        print("TypeError: not int type assigned to int")
        names[p[2]] = 0

    else:
        names[p[2]] = p[5]


def p_statement_bool_assign(p):
    """
    type : KINT
         | KBOOL
         | empty
    """
    p[0] = p[1]


def p_statement_reassign(p):
    """statement : ID "=" expression"""
    if p[1] in names:
        names[p[1]] = p[3]
    else:
        print("Undefined identifier '%s'" % p[1])
        p[0] = 0


def p_empty(p):
    """empty :"""
    pass


def p_statement_expr(p):
    """
    statement : expression
              | condition
    """
    # print(names)
    print(p[1])


def p_expression_binop(p):
    """
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
    """

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_int(p):
    "expression : INT"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined identifier '%s'" % p[1])
        p[0] = 0


def p_condition_binop(p):
    """
    condition : condition LAND condition
              | condition LOR condition
    """

    if p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]


def p_condition_group(p):
    """condition : '(' condition ')'"""
    p[0] = p[2]


def p_condition_unot(p):
    """condition : '!' condition"""
    p[0] = not p[2]


def p_condition_bool(p):
    """condition : BOOL"""
    p[0] = p[1]


def p_condition_relop(p):
    """
    condition : expression LT expression
              | expression LE expression
              | expression GT expression
              | expression GE expression
              | expression EQ expression
              | expression NE expression
    """
    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

# import logging
#
# logging.basicConfig(
#     level=logging.INFO,
#     filename="parse_log.txt"
# )

while True:
    try:
        s = input('stmt > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s, debug=logging.getLogger())
