from ply import lex
from ply import yacc
import sys

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'LCORCHETE','RCORCHETE', 'DESCRIPTOR', 'LLLAVE', 'RLLAVE', 'LPAREN', 'RPAREN'
    ,'DESCRIPTORVALOR','RES','NUMBER','MOVIMIENTO',
    'SIMBOLO', 'COMENTARIO'
    )

# Tokens

t_LCORCHETE    = r'\['
t_RCORCHETE    = r'\]'
t_DESCRIPTOR    = r'[a-zA-Z0-9]+'
t_DESCRIPTORVALOR    = r'\"[^\"]+\"'
t_RES                = r'(1-0|0-1|1\/2-1\/2)'
t_MOVIMIENTO        = r'((P|N|B|R|Q|K)?[a-h]?[1-8]?x?[a-h][1-8])|O-O-O|O-O'
t_SIMBOLO           = r'\+|\+\+|\!|\?'
t_LLLAVE             = r'{'
t_RLLAVE            = r'}'
t_LPAREN             = r'\('
t_RPAREN            = r'\)'
t_COMENTARIO             = r'({[\s\S]*} | \([\s\S]*\))'

def t_NUMBER(t):
    r'\d+\.'
    l = len(t.value)
    t.value = int(t.value[:l-1])
    return t

# Ignored characters
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
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
    '''pgn : LCORCHETE DESCRIPTOR DESCRIPTORVALOR RCORCHETE descriptor_evento NUMBER jugada desc_jugada resultado'''
    if(p[6] != 1):
        raise Exception("La jugada no empieza en 1")


def p_linea_descriptor(p):
    '''descriptor_evento : LCORCHETE DESCRIPTOR DESCRIPTORVALOR RCORCHETE descriptor_evento 
                         | empty'''
    #names[p[1]] = p[3]

def p_jugada(p):
    '''jugada : NUMBER jugada desc_jugada
              | empty'''
    p[0] = p[1]
    if len(p) == 3 and not p[2] is None:
        if p[1] != p[2] - 1:
            raise Exception("Los numeros de jugada no son secuenciales")

def p_desc_jugada(p):
    '''desc_jugada : MOVIMIENTO simbolo comentario movimiento simbolo comentario'''    
    #p[2] = p[0] + 1
    #if(p[2] != p[0] + 1):
    #    raise Exception("Los numeros de jugada no son secuenciales")
    #names[p[1]] = p[3]

def p_movimiento(p):
    '''movimiento : MOVIMIENTO 
                  | empty'''

def p_simbolo(p):
    '''simbolo : SIMBOLO 
                | empty'''

def p_comentario(p):
    '''comentario : COMENTARIO'''
    
#def p_contenido(p):
#    '''contenido : comentario TEXTO comentario 
#                 | empty'''
    
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

    
