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
    'case': 'KCASE',
    'else': 'KELSE',
    'package': 'KPACKAGE',
    'switch': 'KSWITCH',
    'const': 'KCONST',
    'if': 'KIF',
    'func': 'KFUNC',
    'continue': 'KCONTINUE',
    'import': 'KIMPORT',
    'Println': 'KPRINT',
    'fmt': 'KFMT',
    'main': 'KMAIN'
}

# tokens
tokens = (
             'NLD',  # newline
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

t_STRING = r'"[^"]*"'  # accept all string but '"'


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


def t_NLD(t):
    r'[\n]+'
    t.lexer.lineno += t.value.count('\n')
    return t


literals = [
    '=', '+', '-', '*', '/',  # arithmetic(except '=')
    '(', ')',  # parenthesis
    '!',  # logical
    '{', '}', ',', ':', '.'
]

# Ignored characters
t_ignore = ' \t'


# # Ignored token with an action associated with it
# def t_ignore_newline(t):
#     r'\n+'
#     t.lexer.lineno += t.value.count('\n')


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
start = 'start'
is_fmt = not False


# def p_test(p):
#     """
#     test : KPACKAGE KMAIN NLD global_statement import_statement NL
#     """


def p_start(p):  # import statement 추가
    """
    start : KPACKAGE KMAIN NLD global_statement import_statement NLD main_statement
    """
    p[0] = ("start", p[4], p[5], p[7])
    print("Code accepted:", p[0])


def p_import_statement(p):
    """
    import_statement : KIMPORT STRING
    """
    global is_fmt
    if p[2] == '"fmt"':
        is_fmt = True
        print("module", p[2], "imported")

    p[0] = ("import", p[2])


def p_import_statement_empty(p):
    """
    import_statement : empty
    """
    p[0] = ("import", None)


def p_statement(p):
    """
    statement : print_statement statement
              | if_statement statement
              | switch_statement statement
              | for_statement statement
              | assign_statement statement
    """
    p[0] = (p[1], ) + p[2]


def p_statement_empty(p):
    """
    statement : empty
    """
    p[0] = tuple()


def p_main_statement(p):
    """
    main_statement : global_statement KFUNC KMAIN '(' ')' '{' NL statement NL '}'
    """
    p[0] = (p[1], ("main", p[8]), None)


def p_main_statement_with_global(p):
    """
    main_statement : global_statement KFUNC KMAIN '(' ')' '{' NL statement NL '}' NLD global_statement
    """
    p[0] = (p[1], ("main", p[8]), p[12])


def p_NL(p):
    """
    NL : NLD
       | empty
    """


def p_global_statement(p):
    """
    global_statement : global_assign_statement NLD global_statement
    """
    p[0] = (p[1], ) + p[3]


def p_global_statement_empty(p):
    """global_statement : empty"""
    p[0] = tuple()


def p_global_assign_statement(p):  # not implemented
    """
    global_assign_statement : KVAR
    """


def p_if_statement(p):
    """
    if_statement : KIF condition '{' NL statement NL '}' else_statement NLD
    """
    p[0] = (("if", p[2], p[5]), ) + p[8]
    print("If accepted: ", p[0])


def p_else_statement_elif(p):
    """
    else_statement : KELSE KIF condition '{' NL statement NL '}' else_statement
    """
    p[0] = (("else if", p[3], p[6]), ) + p[9]


def p_else_statement_else(p):
    """else_statement : KELSE '{' NL statement NL '}'"""
    p[0] = ("else", p[4])


def p_else_statement_empty(p):
    """else_statement : empty"""
    p[0] = tuple()


def p_switch_statement_cond(p):
    """
    switch_statement : KSWITCH '{' NL case_statement '}' NLD
    """
    p[0] = ("switch", p[4])
    print("Switch accepted: ", p[0])


def p_switch_statement_var(p):
    """
    switch_statement : KSWITCH expr_cond '{' NL case_var_statement '}' NLD
    """
    p[0] = ("switch", p[2], p[5])
    print("Switch accepted: ", p[0])


def p_case_statement(p):
    """
    case_statement : KCASE condition ':' NL statement case_statement
    """
    p[0] = (("case", p[2], p[5]),) + p[6]


def p_case_statement_default(p):
    """case_statement : KDEFAULT ':' NL statement case_without_default_statement"""
    p[0] = (("default", p[4]),) + p[5]


def p_case_statement_empty(p):
    """case_statement : empty"""
    p[0] = tuple()


def p_case_without_default_statement(p):
    """
    case_without_default_statement : KCASE condition ':' NL statement case_without_default_statement
    """
    p[0] = (("case", p[2], p[5]),) + p[6]


def p_case_without_default_statement_empty(p):
    """case_without_default_statement : empty"""
    p[0] = tuple()


def p_case_var_statement(p):
    """
    case_var_statement : KCASE var_statement ':' NL statement case_var_statement
    """
    p[0] = (("case", p[2], p[5]),) + p[6]


def p_case_var_statement_default(p):
    """case_var_statement : KDEFAULT ':' NL statement case_var_without_default_statement"""
    p[0] = (("default", p[4]), ) + p[5]


def p_case_var_statement_empty(p):
    """case_var_statement : empty"""
    p[0] = tuple()


def p_case_var_without_default_statement(p):
    """
    case_var_without_default_statement : KCASE var_statement ':' NL statement case_var_without_default_statement
    """
    p[0] = (("case", p[2], p[5]), ) + p[6]


def p_case_var_without_default_statement_empty(p):
    """case_var_without_default_statement : empty"""
    p[0] = tuple()


def p_var_statement(p):
    """
    var_statement : expr_cond comma_var
    """
    p[0] = (p[1], *p[2][::-1])


def p_comma_var(p):
    """
    comma_var : ',' expr_cond comma_var
    """
    p[0] = p[3] + (p[2], )


def p_var_empty(p):
    """comma_var : empty"""
    p[0] = tuple()


def p_for_statement(p):
    """
    for_statement : KFOR
    """
    pass


def p_assign_statement(p):
    """
    assign_statement : var_assign_statement NLD
                     | const_assign_statement NLD
                     | def_statement NLD
    """
    p[0] = p[1]


def p_assign_statement_default(p):  # add zero value handling / redeclare
    """var_assign_statement : KVAR ID type assign_expr"""
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
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = False  # zero accepted

    elif p[3] == 'int':
        if p[4] is not None:
            if t != int:
                print("TypeError: non int type assigned to int")
            else:
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = 0  # zero accepted

    elif p[3] == 'string':
        if p[4] is not None:
            if t != str:
                print("TypeError: non string type assigned to string")
            else:
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = ""  # zero accepted

    p[0] = ("var", p[2], p[3], p[4])


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


def p_assign_const_statement(p):
    """const_assign_statement : KCONST ID type assign_expr"""
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
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = False  # zero accepted

    elif p[3] == 'int':
        if p[4] is not None:
            if t != int:
                print("TypeError: non int type assigned to int")
            else:
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = 0  # zero accepted

    elif p[3] == 'string':
        if p[4] is not None:
            if t != str:
                print("TypeError: non string type assigned to string")
            else:
                names[p[2]] = p[4]  # Accepted

        else:
            names[p[2]] = ""  # zero accepted

    constants.add(p[2])
    p[0] = ("constant", p[2], p[3], p[4])


def p_def_statement(p):
    """def_statement : ID DEF expr_cond"""
    # redeclared check
    if p[1] in names:
        print(f"Error: {p[1]} redeclared in the scope")
        return

    names[p[1]] = p[3]
    p[0] = ("def", p[1], type(names[p[1]]), p[3])


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
    if not isinstance(names[p[1]], type(p[3])):
        print(f"TypeError: type mismatch {names[p[1]]} and {p[3]}")
        return

    names[p[1]] = p[3]
    p[0] = ("reassign", p[1], type(names[p[1]]), p[3])


def p_statement_reassign_op(p):
    """assign_statement : ID assign_oper expression"""
    # name check
    if p[1] not in names:
        print("Undefined identifier '%s'" % p[1])
        return

    # const check
    if p[1] in constants:
        print(f"Error: cannot assign to constant {p[1]}")
        return

    # type check
    if not isinstance(names[p[1]], type(p[3])):
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

    p[0] = ("reassign_op", p[1], type(names[p[1]]), names[p[1]])


def p_assign_oper(p):
    """
    assign_oper : PE
                | ME
                | TE
                | DE
                | MOE
    """
    p[0] = p[1]


def p_empty(p):
    """empty :"""
    pass


def p_expression_binop(p):
    """expression : expression oper expression"""

    # type check
    if not isinstance(p[1], type(p[3])):
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


def p_oper(p):
    """
    oper : '+'
         | '-'
         | '*'
         | '/'
         | '%'
    """
    p[0] = p[1]


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
    p[0] = p[1].replace('"', '')  #


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
    condition : expression rel_op expression
              | condition EQ condition
              | condition NE condition
    """

    # type check
    if not isinstance(p[1], type(p[3])):
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


def p_rel_op(p):
    """
    rel_op : LT
           | LE
           | GT
           | GE
           | EQ
           | NE
    """
    p[0] = p[1]


def p_print_statement(p):
    """print_statement : KFMT '.' KPRINT '(' expr_cond args ')' NLD"""
    if not is_fmt:
        print("ImportError: 'fmt' is not imported")
        return

    p[0] = ("print", p[5], *p[6][::-1])


def p_args(p):
    """
    args : ',' expr_cond args
    """
    p[0] = p[3] + (p[2], )


def p_args_empty(p):
    """args : empty"""
    p[0] = tuple()


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

# debugging process(stack view)

import logging

logging.basicConfig(
    level=logging.INFO,
    filename="parse_log.txt"
)

# file execution for debug
with open("input.txt") as f:
    yacc.parse(f.read(), debug=logging.getLogger())
    input()
    exit(0)


# # file execution
# if len(sys.argv) == 2:
#     with open(sys.argv[1]) as f:
#         data = f.read()
#
#     yacc.parse(data)
#     exit(0)
#
# # interactive mode
# while True:
#     print(names)
#     try:
#         s = input('stmt > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     # yacc.parse(s, debug=logging.getLogger())
#     yacc.parse(s)
