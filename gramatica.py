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

