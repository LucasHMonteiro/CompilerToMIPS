import re
import ply.lex as lex
import ply.yacc as yacc
 
## Lexer part
# tokens = ( 'LETTER', 'DIGIT', 'SEMI' )
tokens = (
    'INTEGER',
    'ID',
    'OP_REL',
    'OP_ARIT',
    'COMMENT',
    'EQ',
    'SEMI',
    'COL',
    'LPAREN',
    'RPAREN',
    'IF',
    'THEN',
    'ELSE',
    'DEF'
)

def t_INTEGER(t):
    r'[0-9][0-9]*'

def t_ID(t):
    r'[a-zA-Z]([0-9]|[a-zA-Z]|_)*'
    return t

def t_EQ(t):
    r'='
    return t

def t_OP_REL(t):
    r'[>|<|=]'
    return t

def t_OP_ARIT(t):
    r'[+\-*/]'
    return t

def t_COMMENT(t):
    r'//[^\n]*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    return t

def t_SEMI(t):
    r';'
    return t

def t_COL(t):
    r','
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_DEF = r'def'

t_ignore = '[ \n\t\r\f]'

lexer = lex.lex(debug=1)
 
## Parser part
start = 'start'
 
def p_P(p):
    ''' P : ID EQ INTEGER SEMI P 
          | I
    '''
    #print(p[1])

def p_I(p):
    ''' I : D SEMI I
          | D
    '''

def p_D(p):
    ''' D : DEF ID LPAREN ARGS RPAREN EQ E SEMI
    '''

def p_ARGS(p):
    ''' ARGS : ID COL ARGS
             | ID
    '''

def p_SEQ(p):
    ''' SEQ : E
            | SEQ COL E
    '''

def p_E(p):
    ''' E : INTEGER
          | ID
          | IF E OP_REL E THEN E ELSE E
          | E OP_ARIT E
          | ID LPAREN SEQ RPAREN
    '''

start = 'P'
 
parser = yacc.yacc(debug=1)
 
## Test it
s = ''' a = 312;
        b = 111;
        def mdc(a,b) =
            if mod(a,b)= 0
                then b
                else mdc(b,mod(a,b));
        def mod(a,b) =
            if a< b
                then a
                else mod(a-b,b)
    '''
print(parser.parse(s))