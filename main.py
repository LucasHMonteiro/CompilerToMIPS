import re
import ply.lex as lex
import ply.yacc as yacc
 
## Lexer part
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
    t.value = int(t.value)
    return t

t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_DEF = r'def'
t_ID = r'[a-zA-Z]([0-9]|[a-zA-Z]|_)*'
t_EQ = r'='
t_OP_REL = r'[>|<|=]'
t_OP_ARIT = r'[+\-*/]'
t_COMMENT = r'//[^\n]*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COL = r','
t_SEMI = r';'

t_ignore = '[ \n\t\r\f]'

lexer = lex.lex(debug=1)
s = input()
lexer.input(s)
while True:
    token = lexer.token()
    if not token:
        break
    print(token)
## Parser part
start = 'start'
 
def p_P(p):
    ''' P : D F
    '''
    p[0] = (p[1], p[2])

def p_D(p):
    ''' D : ID EQ INTEGER SEMI D
          | ID EQ INTEGER SEMI
    '''

def p_F(p):
    ''' F : DEF ID LPAREN ARGS RPAREN EQ E SEMI F
          | DEF ID LPAREN ARGS RPAREN EQ E SEMI
    '''

def p_ARGS(p):
    ''' ARGS : ID COL ARGS
             | ID
    '''

def p_SEQ(p):
    ''' SEQ : E COL SEQ
            | E
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
print(parser.parse(s))