import ply.lex as lex
import ply.yacc as yacc
import sys

# keywords
reserved = {
    'var': 'KVAR',
    'int': 'KINT',
    'bool': 'KBOOL',
    'string': 'KSTRING',
    'for': 'KFOR',
    'break': 'KBREAK',
    'default': 'KDEFAULT',
    'func': 'KFUNC',
    'select': 'KSELECT',
    'case': 'KCASE',
    'else': 'KELSE',
    'package': 'KPACKAGE',
    'switch': 'KSWITCH',
    'const': 'KCONST',
    'if': 'KIF',
    'type': 'KTYPE',
    'continue': 'KCONTINUE',
    'import': 'KIMPORT',
    'return': 'KRETURN',
    'Println': 'KPRINT',
    'main': 'KMAIN'
}

# tokens
tokens = (
             'LOR', 'LAND',  # logical
             'LE', 'LT', 'GE', 'GT', 'EQ', 'NE',  # relational
             'MOE', 'DEF', 'PE', 'ME', 'TE', 'DE',  # assign

             'ID', 'INT', 'BOOL', 'STRING'  # identifier
         ) + tuple(reserved.values())

t_LOR = r'\|\|'
t_LAND = r'&&'

t_LE = r'<='
t_LT = r'<'
t_GE = r'>'
t_GT = r'>='
t_EQ = r'=='
t_NE = r'!='

t_PE = r'\+='
t_ME = r'-='
t_TE = r'\*='
t_DE = r'/='
t_MOE = r'%='

t_DEF = r':='

t_STRING = r'"[a-zA-Z0-9_]*"'


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
    ('nonassoc', 'PE', 'ME', 'TE', 'DE', 'MOE', 'DEF'),
    ('left', 'LAND', 'LOR'),
    ('right', '!'),

    ['nonassoc', 'LE', 'LT', 'GE', 'GT'],  # do not allow expanding
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS')
)

names = {}
global_names = {}
constants = set()
start = 'assign_statement'
is_fmt = False


def p_start(p):  # import statement 추가
    """
    start : KPACKAGE KMAIN statement import_statement statement main_statement statement
    """


def p_import_statement(p):
    """
    import_statement : KIMPORT STRING
                     | empty
    """
    global is_fmt
    if len(p) == 3 and p[2] == "fmt":
        is_fmt = True


def p_statement(p):
    """
    statement : global_statement statement
              | if_statement statement
              | switch_statement statement
              | for_statement statement
              | func_statement statement
              | assign_statement statement
              | empty
    """


def p_main_statement(p):
    """
    main_statement : KFUNC KMAIN '(' ')' '{' statement '}'
    """


def p_global_statement(p):  # 이름 변경
    """
    global_statement : func_statement global_statement
                     | global_assign_statement global_statement
                     | empty
    """


def p_global_assign_statement(p):  # not implemented
    """
    global_assign_statement : empty
    """


def p_if_statement(p):
    """
    if_statement : empty
    """
    pass


def p_switch_statement(p):
    """
    switch_statement : empty
    """
    pass


def p_for_statement(p):
    """
    for_statement : empty
    """
    pass


def p_func_statement(p):
    """
    func_statement : empty
    """
    pass


def p_assign_statement_default(p):  # add zero value handling / redeclare
    """assign_statement : KVAR ID type assign_expr"""
    # redeclared check
    if p[2] in names:
        print(f"Error: {p[2]} redeclared in the scope")
        return

    t = type(p[4])
    if p[3] == 'bool':
        if p[4] is not None:
            if t != bool:
                print("TypeError: non bool type assigned to bool")
            else:
                names[p[2]] = p[4]

        else:
            names[p[2]] = False  # zero accepted

    elif p[3] == 'int':
        if p[4] is not None:
            if t != int:
                print("TypeError: non int type assigned to int")
            else:
                names[p[2]] = p[4]

        else:
            names[p[2]] = 0  # zero accepted

    elif p[3] == 'string':
        if p[4] is not None:
            if t != str:
                print("TypeError: non string type assigned to string")
            else:
                names[p[2]] = p[4]

        else:
            names[p[2]] = ""  # zero accepted

    else:  # Accepted
        names[p[2]] = p[5]


def p_assign_expr(p):
    """
    assign_expr : "=" expr_cond
                | empty
    """
    if p[1] == '=':
        p[0] = p[2]


def p_type(p):
    """
    type : KINT
         | KBOOL
         | KSTRING
         | empty
    """
    p[0] = p[1]


def p_expr_cond(p):
    """
    expr_cond : expression
              | condition
    """
    p[0] = p[1]


def p_assign_def_statement(p):
    """assign_statement : def_statement"""


def p_assign_const_statement(p):
    """assign_statement : KCONST ID type '=' expression"""
    # redeclared check
    if p[2] in names:
        print(f"Error: {p[2]} redeclared in the scope")
        return

    constants.add(p[2])
    names[p[2]] = p[5]


def p_def_statement(p):
    """def_statement : ID DEF expr_cond"""
    # name check
    if p[1] not in names:
        print("Undefined identifier '%s'" % p[1])
        return

    names[p[1]] = p[3]


def p_statement_reassign(p):
    """assign_statement : ID "=" expr_cond"""
    # name check
    if p[1] not in names:
        print("Undefined identifier '%s'" % p[1])
        return

    # const check
    if p[1] in constants:
        print(f"Error: cannot assign to constant {p[1]}")
        return

    # type check
    if isinstance(names[p[1]], type(p[3])):
        print(f"TypeError: type mismatch {names[p[1]]} and {p[3]}")
        return

    names[p[1]] = p[3]


def p_statement_reassign_op(p):
    """
    assign_statement : ID PE expression
                     | ID ME expression
                     | ID TE expression
                     | ID DE expression
                     | ID MOE expression
    """
    # name check
    if p[1] not in names:
        print("Undefined identifier '%s'" % p[1])
        return

    # const check
    if p[1] in constants:
        print(f"Error: cannot assign to constant {p[1]}")
        return

    # type check
    if isinstance(names[p[1]], type(p[3])):
        print(f"TypeError: type mismatch {names[p[1]]}({type(names[p[1]])}) and {p[3]}({type(p[3])})")
        return

    # string check
    if type(names[p[1]]) == str and p[2] != '+=':
        print("Invalid operation:", p[2], "is not defined on string")
        return

    if p[2] == '+=':
        names[p[1]] += p[3]
    elif p[2] == '-=':
        names[p[1]] -= p[3]
    elif p[2] == '*=':
        names[p[1]] *= p[3]
    elif p[2] == '/=':
        if p[3] == 0:  # zero division check
            print("ZeroDivisionError: division by zero")
            return
        names[p[1]] //= p[3]
    elif p[2] == '%=':
        if p[3] == 0:  # zero division check
            print("ZeroDivisionError: division by zero")
            return
        names[p[1]] %= p[3]


def p_empty(p):
    """empty :"""
    pass


def p_expression_binop(p):
    """
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression '%' expression
    """

    # type check
    if isinstance(p[1], type(p[3])):
        print(f"TypeError: type mismatch {p[1]} and {p[3]}")
        p[0] = 0
        return

    # string check
    if type(p[1]) == str and p[2] != '+':
        print("Invalid operation:", p[2], "is not defined on string")
        return

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:  # zero division check
            print("ZeroDivisionError: division by zero")
            p[0] = 0
            return
        p[0] = p[1] // p[3]
    elif p[2] == '%':
        if p[3] == 0:  # zero division check
            print("ZeroDivisionError: division by zero")
            p[0] = 0
            return
        p[0] = p[1] % p[3]


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = -p[2]


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_int(p):
    """
    expression : INT
    """
    p[0] = p[1]


def p_expression_string(p):
    """
    expression : STRING
    """
    p[0] = p[1].replace('"', '')


def p_expression_id(p):
    """expression : ID"""
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
              | condition EQ condition
              | condition NE condition
    """

    # type check
    if isinstance(p[1], type(p[3])):
        print(f"TypeError: type mismatch {p[1]} and {p[3]}")
        p[0] = False
        return

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

# debugging process(stack view)

# import logging
#
# logging.basicConfig(
#     level=logging.INFO,
#     filename="parse_log.txt"
# )


# file execution
if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        data = f.read()

    yacc.parse(data)
    exit(0)

# interactive mode
while True:
    print(names)
    try:
        s = input('stmt > ')
    except EOFError:
        break
    if not s:
        continue
    # yacc.parse(s, debug=logging.getLogger())
    yacc.parse(s)
