# Este programa python recebe uma lista de pares ordenados definindo trechos de um pequeno video, por exemplo
# [ (   49   , 80 )   , ( 600  , 1013   )   , ( 42   , 78 ) , ( 449 , 557 )  , ( 852  , 961    ) , ( 111  , 119   )   , ( 77   , 139    ) ].
# Cada par é da forma (frame inicial, frame final). Observe que os trechos estao desordenados e se sobrepõe.

#O objetivo deste código é gerar um nova lista que contemple todos os trechos da lista, em ordem e sem sobreposição.

#Assim uma lista de entrada [( 49 , 80 )  e ( 42 , 78 )] retorna a saída [(42,80)]

# Revisao 1: Sintaxe:           Comando "return" nao tem a mesma identacao da definicao da funcao, "def" e sim a dos comandos da funcao que terminam em sua declaração
# Revisao 2: Legibilidade:      Nomeclatura baseada a tipos de dados, sem referencia a funcao de cada dado, dificulta entendimento do codigo, prejudicando manutenção e evolução

def NormalizaLista ( Lista1 )   :
    Lista2 = [ ]
    for Tupla1 in Lista1  :                                                 
            if not Lista2  :                                                        
                Lista2.append  (   Tupla1 )                                  
            else    :                                                                                
                Tupla2 = Lista2    [   -   1   ]                                         
                if Tupla1  [   0   ] <= Tupla2 [   1   ]   :                                 
                    Numero1 = max   (   Tupla2  [   1   ]   , Tupla1   [   1   ]   ) 
                    Lista2 [   -   1   ] = (   Tupla2  [   0   ]   , Numero1   )  
                else    :
                    Lista2.append  (   Tupla1 )                                      
    Lista1 = sorted  (   Lista2    ,   key=lambda Par  : Par   [   0   ]   ) 
    return Lista1
