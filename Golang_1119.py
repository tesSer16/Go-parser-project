from ply.lex import lex
from ply.yacc import yacc

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULAR', 'LT','LE','GT','GE','EQ','NE',
            #'DOUBLEPLUS','DOUBLEMINUS',
            'LOGAND',
            #'LOGOR',
            'LOGNOT','LPAREN', 'RPAREN','INTEGER','STRING','BOOLEAN' )
#주석처리 한 애들 -> 넣으면 LEX가 안됨

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_MODULAR = r'\%'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
#t_DOUBLEPLUS = r'++'
#t_DOUBLEMINUS = r'--'
t_LOGAND = r'&&'
#t_LOGOR = r'||'
t_LOGNOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
#t_UPLUS = r'\+'
#t_UMINUS = r'\-'

#주석처리 한 애들 -> 넣으면 LEX가 안됨


precedence = (
    #('left','LOGOR'),
    ('left','LOGAND'),
    ('left','EQ','NE','LT',"LE","GT","GE"),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULAR'),
    #('right','UPLUS','UMINUS'),
    ('left','LPAREN','RPAREN')
)


# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = str(t.value)
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = bool(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
    
lexer = lex()

lexer.input("1+(2+3)%4<=&&\"ASDF\"true")
while(True):
    token = lexer.token()
    if not token:
        break
    print(token)

# --- Parser


# Write functions for each grammar rule which is
# specified in the docstring.

#def p_unary_integer(p):
#    '''integer -> PLUS integer %prec UPLUS
#                | MINUS integer  %prec UMINUS'''
#    if p[1] == '+':
#        p[0] = p[2]
#    elif p[2] == '-':
#        p[0] = -p[2]

# 여기서 부터 PARSER. LEX는 잘 되는데 PARSING은 문제가 많네요.
# 계속 오류가 떠서 일단 작업하던 부분 전부 주석처리해놨습니다.    
# 손으로 Parsing했을 때는 원하는 곳에 원하는 변수를 넣을 수 있었는데 여기선 어떻게 하는지 잘 모르겠네요...
# Boolean -> Integer EQ Integer 같은 경우에서 p[0]에 bool값을, p[1]과 p[3]에 integer값을 넣는 방법을 모르겠습니다.
# 이 파트 유의하면서 계속 작업하겠습니다.
    
"""  

def p_integer_compare(p):
    '''boolean -> integer EQ integer
                | integer NE integer
                | integer LT integer
                | integer LE integer
                | integer GT integer
                | integer GE integer'''
    if p[2] == '==':
        p[0] = (p[1] == p[3])  
    elif p[2] == '!=':
        p[0] = (p[1] != p[3])  
    elif p[2] == '<':
        p[0] = (p[1] < p[3])  
    elif p[2] == '<':
        p[0] = (p[1] <= p[3])  
    elif p[2] == '>':
        p[0] = (p[1] > p[3])  
    elif p[2] == '>=':
        p[0] = (p[1] >= p[3])

def p_integer_logical(p):
    '''boolean -> boolean LOGAND boolean'''   
    if p[2] == "&&":
        p[0] = (p[1] and p[3])

def p_integer_arthimetric(p):
    '''integer -> integer PLUS integer
                | integer MINUS integer
                | integer TIMES integer
                | integer DIVIDE integer
                | integer MODULAR integer'''  
    if p[2] == '+':
        p[0] = p[1] + p[3] 
    elif p[2] == '-':
        p[0] = p[1] - p[3] 
    elif p[2] == '*':
        p[0] = p[1] * p[3] 
    elif p[2] == '/':
        p[0] = p[1] / p[3] 
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_factor_integer(p):
    '''
    factor : INTEGER
    '''
    p[0] = ('integer', p[1])


def p_factor_string(p):
    '''
    factor : string
    '''
    p[0] = ('string', p[1])

def p_factor_boolean(p):
    '''
    factor : boolean
    '''
    p[0] = ('boolean', p[1])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast) """