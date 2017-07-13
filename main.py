import ply.lex as lex
import ply.yacc as yacc
import itertools
from cgen import CGen

cgen = CGen()

def cat_list(init_list, list_end):
    if type(list_end) == type([]):
        return init_list + list_end
    else:
        init_list.append(list_end)

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
args_hash = {}
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
    global args_hash
    if len(p) > 2:
        first = {p[1]: len(p[3])+1}
        first.update(args_hash)
        args_hash.update(first)
        p[0] = [p[1]]
        p[0].append(p[3])
        p[0] = list(itertools.chain(*p[0]))
        if len(set(p[0])) < len(p[0]):
            raise Exception('Duplicate arguments given')
        global args_list
        args_list = p[0]
    else:
        global args_hash
        args_hash = {p[1]: 1}
        p[0] = p[1]

def p_SEQ(p):
    ''' SEQ : E COL SEQ
            | E
    '''
    if len(p) > 2:
        p[0] = [p[1]]
        cat_list(p[0], p[3])
    else:
        p[0] = p[1]

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
            if not len(p[3]) == len(symbol_table[p[1]]):
                raise Exception("Wrong number of parameters expected: %d, given: %s" % (len(symbol_table[p[1]]), p[3]))

    global args_hash
    if not p.slice[1].type == 'ARIT_EXP':
        print(cgen.e(p, args_hash))
    args_hash = {}

def p_ARIT_EXP(p):
    ''' ARIT_EXP : ARIT_EXP OP_ADD TERM
                 | TERM
    '''
    if len(p) > 2:
        cgen.arit(p)

def p_TERM(p):
    ''' TERM : TERM OP_MULT FACTOR
             | FACTOR
    '''
    if len(p) > 2:
        cgen.term(p)

def p_FACTOR(p):
    ''' FACTOR : PAREN
               | E
    '''

def p_PAREN(p):
    ''' PAREN : LPAREN E RPAREN
    '''
    cgen.paren(p)

def p_error(p):
    print("Syntax error at token '%s' of type '%s' at position '%s'" % (p.value, p.type, p.lexpos))

start = 'P'

parser = yacc.yacc(debug=1)

## Test it
s = ''' a = 1;
        b = 2;
        def sum(a,b) =
            a + b;
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
