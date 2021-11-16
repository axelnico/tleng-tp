Gramatica

pgn -> LCORCHETE DESCRIPTOR DESCRIPTORVALOR RCORCHETE descriptor_evento NUMBER desc_jugada jugada resultado

jugada.orden = 1

if(NUMBER == 1)


'''descriptor_evento : LCORCHETE DESCRIPTOR DESCRIPTORVALOR RCORCHETE descriptor_evento 
                         | empty'''

jugada1 -> NUMBER desc_jugada jugada

jugada = jugada1.orden + 1
if(NUMBer == jugada1.orden + 1) 


jugada -> .

resultado -> 1-0|0-1|1/2-1/2

pgn ->  NUMBER jugada -> NUMBER NUMBER jugada -> NUMBER NUMBER NUMBER jugada -> NUMBER NUMBER NUMBER 


desc_jugada ->  MOVIMIENTO simbolo comentario movimiento simbolo comentario 

simbolo -> SIMBOLO | .

movimiento -> MOVIMIENTO | .

comentario -> LLLAVE contenido RLLAVE | LPAREN contenido RPAREN | .

contenido -> comentario TEXTO comentario | .



Preguntas:

Como hacemos para tokenizar el texto? Tenemos problemas con el texto libre de los comentarios, porque podria aparecer una jugada por ejemplo
La tokenizacion puede hacer que la misma cadena aparezca en dos o mas tokens? 

si se definen como funciones 

La gramatica es LALR esta bien planteado lo del numero? no se pueden usar atributos heredados por el orden del parsing?
Esta bien planteada las reglas de la gramatica? se considera a todo como un unico texto?
Nota de pie de pagina, con respecto al simbolo =, en la pagina 2
Que mostrar por pantalla
Que solo la ultima jugada tengo un movimiento o puede tener otra jugada anterior un solo movimiento
Los descriptores de evento es solo una palabra? puede tener cualquier simbolo? lo mismo para el valor del descriptor? Es obligatorio
que haya al menos uno
