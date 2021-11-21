from tokens import *

t_DESCRIPTOR    = r'\[[^\[\]]+ \"[^\[\]]+\"\]'
t_RES                = r'(1-0|0-1|1\/2-1\/2)'
t_SIMBOLO           = r'\+|\+\+|\!|\?'

comentarios_abiertos  = 0

# States
states = (
    ('insideComment','exclusive'),
)

def t_insideComment_INITIAL_MOVIMIENTO(t):
    r'((P|N|B|R|Q|K)?[a-h]?[1-8]?x?[a-h][1-8])|O-O-O|O-O'
    return t


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
t_insideComment_ignore = ' '

def t_insideComment_TEXTO(t):
    r'[^\{\}\(\)\s]+'
    return t

def t_insideComment_INITIAL_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_insideComment_INITIAL_error(t):
    raise Exception(f"Carácter inválido {t.value[0]!r} en linea {t.lexer.lineno}")
