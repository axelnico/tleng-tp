from ply import lex
from ply import yacc
import sys

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'DESCRIPTOR', 'LLLAVE', 'RLLAVE', 'LPAREN', 'RPAREN','RES','NUMBER','MOVIMIENTO',
    'SIMBOLO', 'TEXTO', 'CONTINUAJUGADA'
    )

# Tokens

t_DESCRIPTOR    = r'\[[^\[\]]+ \"[^\[\]]+\"\]'
t_RES                = r'(1-0|0-1|1\/2-1\/2)'
t_MOVIMIENTO        = r'((P|N|B|R|Q|K)?[a-h]?[1-8]?x?[a-h][1-8])|O-O-O|O-O'
t_SIMBOLO           = r'\+|\+\+|\!|\?'

comentarios_abiertos  = 0

# States
states = (
    ('insideComment','exclusive'),
)

def t_insideComment_INITIAL_LLLAVE(t):
    r'{'
    global comentarios_abiertos
    comentarios_abiertos +=1
    t.lexer.begin('insideComment')
    return t


def t_insideComment_INITIAL_RLLAVE(t):
    r'}'
    global comentarios_abiertos
    comentarios_abiertos -=1
    if comentarios_abiertos == 0:
        t.lexer.begin('INITIAL')
    return t

def t_insideComment_INITIAL_LPAREN(t):
    r'\('
    global comentarios_abiertos
    comentarios_abiertos +=1
    t.lexer.begin('insideComment')
    return t

def t_insideComment_INITIAL_RPAREN(t):
    r'\)'
    global comentarios_abiertos
    comentarios_abiertos -=1
    if comentarios_abiertos == 0:
        t.lexer.begin('INITIAL')
    return t

def t_CONTINUAJUGADA(t):
    r'\d+\.\.\.'
    l = len(t.value)
    t.value = int(t.value[:l-3])
    return t

def t_NUMBER(t):
    r'\d+\.'
    l = len(t.value)
    t.value = int(t.value[:l-1])
    return t


# Ignored characters
t_ignore = ' \t'
t_insideComment_ignore = ''

def t_insideComment_TEXTO(t):
    r'[^\{\}\(\)]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

def t_insideComment_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Precedence rules for the arithmetic operators
#precedence = (
#    ('left','PLUS','MINUS'),
#    ('left','TIMES','DIVIDE'),
#    ('right','UMINUS'),
#    )

# dictionary of names (for storing variables)
#names = { }

def p_inicio_pgn(p):
    '''pgn : DESCRIPTOR descriptor NUMBER desc_jugada jugada resultado partida'''
    if p[3] != p[4] and p[4] is not None:
        raise Exception("Continuacion de jugada incorrecta")
    if(p[3] != 1):
        raise Exception("La jugada no empieza en 1")

def p_partida(p):
    '''partida : DESCRIPTOR descriptor NUMBER desc_jugada jugada resultado partida
               | empty'''
    if len(p) == 3:
        if p[3] != p[4] and p[4] is not None:
            raise Exception("Continuacion de jugada incorrecta")
    if len(p) > 2 and  p[3] != 1:
        raise Exception("La jugada no empieza en 1")

def p_linea_descriptor(p):
    '''descriptor : DESCRIPTOR descriptor
                  | empty'''
    #names[p[1]] = p[3]

def p_jugada(p):
    '''jugada : NUMBER desc_jugada jugada
              | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if p[1] != p[2] and p[2] is not None:
            raise Exception("Continuacion de jugada incorrecta")
    if len(p) == 3 and not p[3] is None:
        if p[1] != p[3] - 1:
            raise Exception("Los numeros de jugada no son secuenciales")

def p_desc_jugada(p):
    '''desc_jugada : MOVIMIENTO simbolo comentario_siguiente_jugada movimiento simbolo comentario'''
    p[0] = p[3]
    #p[3] = p[0]    
    #p[2] = p[0] + 1
    #if(p[2] != p[0] + 1):
    #    raise Exception("Los numeros de jugada no son secuenciales")
    #names[p[1]] = p[3]

def p_comentario_con_siguiente_jugada(p):
    '''comentario_siguiente_jugada : LLLAVE contenido RLLAVE CONTINUAJUGADA
                                   | LPAREN contenido RPAREN CONTINUAJUGADA
                                   | empty'''
    if len(p) == 5:
        p[0] = p[4]

def p_movimiento(p):
    '''movimiento : MOVIMIENTO 
                  | empty'''

def p_simbolo(p):
    '''simbolo : SIMBOLO 
               | empty'''

def p_comentario(p):
    '''comentario : LLLAVE contenido RLLAVE
                  | LPAREN contenido RPAREN
                  | empty'''

def p_contenido(p):
    '''contenido : contenido TEXTO contenido 
                 | comentario
                 | empty'''
    
def p_resultado(p):
    '''resultado : RES'''

def p_empty(p):
    'empty :'
    pass
#def p_statement_expr(p):
#    'statement : expression'
#    print(p[1])

#def p_expression_binop(p):
#    '''expression : expression PLUS expression
#                  | expression MINUS expression
#                  | expression TIMES expression
#                  | expression DIVIDE expression'''
#    if p[2] == '+'  : p[0] = p[1] + p[3]
#    elif p[2] == '-': p[0] = p[1] - p[3]
#    elif p[2] == '*': p[0] = p[1] * p[3]
#    elif p[2] == '/': p[0] = p[1] / p[3]

''' def p_expression_uminus(p):
   'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

'''
def p_error(p):
    if p is None:
        print("Parsing error")
    else:
        print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()


#lex.runmain()

data = sys.stdin.read()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

yacc.parse(data,debug=False)

    
