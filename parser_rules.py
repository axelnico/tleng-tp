from tokens import *

# Contiene las reglas para la produccion de las jugadas
# p[0] = jugada
# p[1] = NUMBER
# p[2] = desc_jugada
# p[3] = jugada
# p[4] = resultado
def gramar_rules_jugada(p):
    if p[2]["continua_jugada"] != 0 and p[1] != p[2]["continua_jugada"]:
        raise Exception(f"Error. Continuacion de jugada incorrecta: {p[2]['continua_jugada']} y {p[1]} en linea {p.lineno(1)}")
    if p[3]["numero_jugada"] is not None:
        # Esta rama del condicional significa que se trata de una jugada que no es la ultima
        if p[1] != p[3]["numero_jugada"] - 1:
            raise Exception(f"Error. Los numeros de jugada no son secuenciales: {p[3]['numero_jugada']} y {p[1]} en linea {p.lineno(1)}")
        if p[2]["cant_movimientos"] == 1:
            raise Exception(f"Error. Solo el ultimo movimiento puede jugar solo negras o blancas: En jugada {p[1]} en linea {p.lineno(2)}")
        if p[4] is not None:
            raise Exception(f"Error. El resultado del partido solo puede estar al final: {p[4]} en jugada {p[1]} en linea {p.lineno(4)}")
    else:
        # Esta rama del condicional significa que se trata de la ultima jugada por lo que es necesario el resultado
        if p[4] is None:
            raise Exception(f"Error. Falta el resultado del partido: En linea {p.lineno(1)}")

# Devuelve los atributos de las producciones de jugadas
# p[0] = jugada
# p[1] = NUMBER | empty
# p[2] = desc_jugada | None
# p[3] = jugada | None
# p[4] = resultado | None
def atributos_jugada(p):
    max_nivel_sin_capturas = 0
    if len(p) > 2:
        max_nivel_sin_capturas = max(p[2]["maximo_nivel_sin_capturas"],p[3]["maximo_nivel_sin_capturas"])
    return {
        'maximo_nivel_sin_capturas': max_nivel_sin_capturas,
        'numero_jugada': p[1]
    } 


# Producción inicial: Representa el archivo PGN, con al menos un partido
def p_inicio_pgn(p):
    '''pgn : header jugadas partida'''
    if p[2]["numero_jugada"] != 1:
        raise Exception(f"La jugada no empieza en 1: {p[2]['numero_jugada']} en linea {p.lineno(2)}")
    print(f"Máximo nivel sin capturas: {max(p[2]['maximo_nivel_sin_capturas'],p[3])}.")

# Producción que representa una serie de jugadas. Al menos tiene que haber una
def p_jugadas(p):
    '''jugadas : NUMBER desc_jugada jugada resultado'''   
    p[0] = atributos_jugada(p)
    gramar_rules_jugada(p)
            

# Producción para generar los descriptores. Al menos siempre tiene que haber uno
def p_header(p):
    '''header : DESCRIPTOR descriptor'''

# Producción que genera partidas de ajedrez
def p_partida(p):
    '''partida : header jugadas partida
               | empty'''
    max_nivel_sin_capturas = 0     
    if len(p) > 2:
        if p[2]["numero_jugada"] != 1:
            raise Exception(f"La jugada no empieza en 1: {p[2]['numero_jugada']} en linea {p.lineno(2)}")
        max_nivel_sin_capturas = max(p[2]["maximo_nivel_sin_capturas"],p[3])
    p[0] = max_nivel_sin_capturas

# Producción para descriptores
def p_linea_descriptor(p):
    '''descriptor : DESCRIPTOR descriptor
                  | empty'''
 
# Producción para jugadas
def p_jugada(p):
    '''jugada : NUMBER desc_jugada jugada resultado
              | empty'''        
    p[0] = atributos_jugada(p)
    if len(p) == 5:
        gramar_rules_jugada(p)
                
# Producción para el cuerpo de las jugadas. Puede ser de uno o dos movimientos
def p_desc_jugada(p):
    '''desc_jugada : MOVIMIENTO simbolo comentario_siguiente_jugada movimiento simbolo comentario'''
    attributes = {
        'continua_jugada': p[3]["continua_jugada"],
        'cant_movimientos': 1,
        'maximo_nivel_sin_capturas': max(p[6]["anidamiento"],p[3]["anidamiento"])
    }
    if p[4] is not None:
        attributes['cant_movimientos'] = 2
    p[0] = attributes

# Producción para los comentarios que incluyen el número de la jugada a la cual corresponden al final, porque la jugada continua
def p_comentario_con_siguiente_jugada(p):
    '''comentario_siguiente_jugada : LLLAVE contenido RLLAVE CONTINUAJUGADA
                                   | LPAREN contenido RPAREN CONTINUAJUGADA
                                   | empty'''
    attributes = {
        'continua_jugada': 0,
        'anidamiento': 0
    }
    if len(p) == 5:
        # Si el comentario no tiene captura o si tiene captura pero ya hay un comentario mas interno que no las contiene entonces se incrementa en uno el nivel
        if not p[2]["tiene_captura"] or not p[2]["anidamiento"] == 0:
            attributes['anidamiento'] = p[2]["anidamiento"] + 1
            attributes['continua_jugada'] = p[4]
    p[0] = attributes

# Producción que representa un movimiento
def p_movimiento(p):
    '''movimiento : MOVIMIENTO 
                  | empty'''
    p[0] = p[1]

# Producción que representa un simbolo
def p_simbolo(p):
    '''simbolo : SIMBOLO 
               | empty'''

# Producción para los comentarios que vienen despúes de la segunda jugada, que no pueden tener otra jugada al final
def p_comentario(p):
    '''comentario : LLLAVE contenido RLLAVE
                  | LPAREN contenido RPAREN
                  | empty'''
    attributes = {
        'tiene_captura': False,
        'anidamiento': 0
    }  
    if len(p) == 4:
        # Si el comentario no tiene captura o si tiene captura pero ya hay un comentario mas interno que no las contiene entonces se incrementa en uno el nivel
        if not p[2]["tiene_captura"] or not p[2]["anidamiento"] == 0:
            attributes['anidamiento'] = p[2]["anidamiento"] + 1
    p[0] = attributes

# Producción para el contenido de los comentarios. Un comentario puede tener cualquier cadena en su interior, con o sin comentarios intercalados
def p_contenido(p):
    '''contenido : contenido cadena contenido 
                 | comentario
                 | empty'''
    attributes = {
        'tiene_captura': False,
        'anidamiento': 0
    }             
    if len(p) == 4:
        attributes['tiene_captura'] = p[1]["tiene_captura"] or p[2] or p[3]["tiene_captura"]
        attributes['anidamiento'] = max(p[1]["anidamiento"],p[3]["anidamiento"]) 
    elif p[1] is not None:
        attributes['anidamiento'] = p[1]["anidamiento"]
    p[0] = attributes


# Producción para las cadenas dentro de los comentarios que pueden ser texto o movimientos
def p_cadena(p):
    '''cadena : texto cadena
              | jugada_en_comentario cadena
              | empty'''
    if len(p) == 2:
        p[0] = False
    else:
        p[0] = p[1] or p[2]

# Producción que representa texto, sin movimientos
def p_texto(p):
    '''texto : TEXTO'''
    p[0] = False

# Producción que representa un movimiento, dentro de un comentario
def p_jugada_en_comentario(p):
    '''jugada_en_comentario : MOVIMIENTO'''
    if not "x" in p[1]:
        p[0] = False
    else:
        p[0] = True

# Producción que representa el resultado de una partida de ajedrez
def p_resultado(p):
    '''resultado : RES 
                 | empty '''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p is None:
        print("Error de parsing")
    else:
        print(f"Error de sintaxis: {p.value!r} en la linea {p.lineno!r}")