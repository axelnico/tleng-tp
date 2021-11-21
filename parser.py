from ply import lex
from ply import yacc

import lexer_rules
import parser_rules
import sys

# ------------------------------------------------------------------------------------------------------------------
# Validación de archivos PGN
#
# Simple validor de sintaxis superficial de archivos PGN y determinación de máximo nivel de comentarios sin capturas.
# ------------------------------------------------------------------------------------------------------------------

# Construimos el lexer
lexer = lex.lex(module=lexer_rules)

# Contruimos el parser
yacc.yacc(module=parser_rules)

# Leemos la entrada estandar
data = sys.stdin.read()

# Le damos al lexer la data leida de la entrada estandar
lexer.input(data)

try:
    yacc.parse(data,debug=False)
except Exception as err: 
    print(err)


    
