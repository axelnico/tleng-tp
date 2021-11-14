from ply import lex
from ply import yacc
import sys

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'LCORCHETE','RCORCHETE',
    'DESCRIPTOR','DESCRIPTORVALOR'
    )

# Tokens

t_LCORCHETE    = r'\['
t_RCORCHETE    = r'\]'
t_DESCRIPTOR    = r'[a-zA-Z0-9\s]+'
t_DESCRIPTORVALOR    = r'\"[a-zA-Z0-9\s]+\"'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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

def p_linea_descriptor(p):
    '''descriptor_evento : LCORCHETE DESCRIPTOR DESCRIPTORVALOR RCORCHETE descriptor_evento 
                         | empty'''
    #names[p[1]] = p[3]

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
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()


#lex.runmain()

data = sys.stdin.read()

# Give the lexer some input
lexer.input(data)

# Tokenize
'''while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
'''
yacc.parse(data)

    
