import ply.lex as lex
import ply.yacc as yacc

## Lexer part

tokens = []

keywordlist = ['if', 'then', 'else', 'def']

RESERVED = {}
for keyword in keywordlist:
	name = keyword.upper()
	RESERVED[keyword] = name
	tokens.append(name)

tokens = tuple(tokens) +\
         (
         'INTEGER',
         'ID',
         'OP_REL',
         'OP_ADD',
         'OP_MULT',
         'COMMENT',
         'EQ',
         'SEMI',
         'COL',
         'LPAREN',
         'RPAREN'
         )

def t_INTEGER(t):
    r'[0-9][0-9]*'
    t.value = int(t.value)
    return t

def t_ID(t):
   r'[a-zA-Z]([0-9]|[a-zA-Z]|_)*'
   t.type = RESERVED.get(t.value, "ID")
   return t

t_EQ = r'='
t_OP_REL = r'[>|<]|=='
t_OP_ADD = r'[\+\-]'
t_OP_MULT = r'[\*\/]'
t_COMMENT = r'//[^\n]*|/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COL = r','
t_SEMI = r';'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_DEF = r'def'

t_ignore = '[ \n\t\r\f]'

def t_error(t):
    print("Illegal character '%s' at line' %s'" % (t.value[0] , t.lexer.lineno ))
    t.lexer.skip(1)

lexer = lex.lex(debug=1)

## Parser part

def p_P(p):
    ''' P : ID EQ INTEGER SEMI P
          | I
    '''
    print(p.slice)
    if len(p) == 6:
        p[0] = p[5]
    else:
        p[0] = p[1]

def p_I(p):
    ''' I : D I
          | D
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
    print(p.slice)
    
def p_D(p):
    ''' D : DEF ID LPAREN ARGS RPAREN EQ E SEMI
    '''
    print(p.slice)    
    p[0] = p[7]

def p_ARGS(p):
    ''' ARGS : ID COL ARGS
             | ID
    '''
    print(p.slice)    
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_SEQ(p):
    ''' SEQ : E COL SEQ
            | E
    '''
    print(p.slice)    
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_E(p):
    ''' E : INTEGER
          | ID
          | IF E OP_REL E THEN E ELSE E
          | ARIT_EXP
          | ID LPAREN SEQ RPAREN
    '''
    print(p.slice)    
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_ARIT_EXP(p):
    ''' ARIT_EXP : ARIT_EXP OP_ADD TERM
                 | TERM
    '''
    print(p.slice)    
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_TERM(p):
    ''' TERM : TERM OP_MULT FACTOR
             | FACTOR
    '''
    print(p.slice)    
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_FACTOR(p):
    ''' FACTOR : PAREN
               | E
    '''
    print(p.slice)    
    p[0] = p[1]

def p_PAREN(p):
    ''' PAREN : LPAREN E RPAREN
    '''
    print(p.slice)    
    p[0] = p[2]

def p_error(p):
    print("Syntax error at token '%s' of type '%s' at position '%s'" % (p.value, p.type, p.lexpos))

start = 'P'

parser = yacc.yacc(debug=1)

## Test it
s = ''' a = 312;
        b = 111;
        def mdc(a,b) =
            if mod(a,b) == 0
            then b
            else mdc(b,mod(a,b));
        def mod(a,b) =
            if a < b
            then a
            else mod(a-b,b);
    '''
# lexer.input(s)
# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)

print(parser.parse(s))
