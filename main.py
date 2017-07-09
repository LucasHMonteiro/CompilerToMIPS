import ply.lex as lex
import ply.yacc as yacc
import itertools

func_hash = {
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '==': lambda x, y: x == y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y
}

symbol_table = {}
first_pass = True
var_list = []
args_list = []
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
    if len(p) > 2:
        global var_list
        if not p[1] in var_list:
            var_list.append(p[1])
        if not set(var_list) == set(args_list) and p.slice[1].lexpos == 1:
            raise Exception('Arguments in the first function not declared')

def p_I(p):
    ''' I : D I
          | D
    '''    

def p_D(p):
    ''' D : DEF ID LPAREN ARGS RPAREN EQ E SEMI
    '''

    if first_pass:
        if p[2] in symbol_table:
            raise Exception('Function name already used')
        symbol_table[p[2]] = p[4]
    else:
        global var_list
        if not set(p[4]) == set(var_list):
            msg = ''
            for id in set(var_list) - set(p[4]):
                msg += 'Variable '+id+' not declared\n'
            raise Exception(msg)
        var_list = []
    
def p_ARGS(p):
    ''' ARGS : ID COL ARGS
             | ID
    '''
    if len(p) > 2:
        p[0] = [p[1]]
        p[0].append(p[3])
        p[0] = list(itertools.chain(*p[0]))
        if len(set(p[0])) < len(p[0]):
            raise Exception('Duplicate arguments given')
        global args_list
        args_list = p[0]
    else:
        p[0] = p[1]

def p_SEQ(p):
    ''' SEQ : E COL SEQ
            | E
    '''
    if len(p) > 2:
        p[0] = 1 + p[3]
    else:
        p[0] = 1

def p_E(p):
    ''' E : INTEGER
          | ID
          | IF E OP_REL E THEN E ELSE E
          | ARIT_EXP
          | ID LPAREN SEQ RPAREN
    '''
    
    if p.slice[1].type == 'ID' and len(p) == 2 and not first_pass:
       global var_list
       if not p[1] in var_list:
           var_list.append(p[1])

    if len(p) == 5 and not first_pass :
        if p[1] not in symbol_table:
            raise Exception('Function not declared')
        else:
            if not p[3] == len(symbol_table[p[1]]):
                raise Exception("Wrong number of parameters expected: %d, given: %s" % (len(symbol_table[p[1]]), p[3]))

def p_ARIT_EXP(p):
    ''' ARIT_EXP : ARIT_EXP OP_ADD TERM
                 | TERM
    '''

def p_TERM(p):
    ''' TERM : TERM OP_MULT FACTOR
             | FACTOR
    '''

def p_FACTOR(p):
    ''' FACTOR : PAREN
               | E
    '''

def p_PAREN(p):
    ''' PAREN : LPAREN E RPAREN
    '''

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
        def fuck(a) = a;
    '''
# lexer.input(s)
# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)

parser.parse(s)
first_pass = False
print(parser.parse(s))
