# Este programa python recebe uma lista de pares ordenados definindo trechos de um pequeno video, por exemplo
# [ (   49   , 80 )   , ( 600  , 1013   )   , ( 42   , 78 ) , ( 449 , 557 )  , ( 852  , 961    ) , ( 111  , 119   )   , ( 77   , 139    ) ].
# Cada par é da forma (frame inicial, frame final). Observe que os trechos estao desordenados e se sobrepõe.

#O objetivo deste código é gerar um nova lista que contemple todos os trechos da lista, em ordem e sem sobreposição.

#Assim uma lista de entrada [( 49 , 80 )  e ( 42 , 78 )] retorna a saída [(42,80)]

# Revisao 1: Sintaxe:           Comando "return" nao tem a mesma identacao da definicao da funcao, "def" e sim a dos comandos da funcao que terminam em sua declaração
# Revisao 2: Legibilidade:      Nomeclatura baseada a tipos de dados, sem referencia a funcao de cada dado, dificulta entendimento do codigo, prejudicando manutenção e evolução
# Revisao 3: Logica/Correção:   A verificacao da relacao entre os trechos ocorre corretamente, porém na ordem que informados. Sobreposicoes entre trechos que  estiveremm disjuntos não são detectadas
# Revisao 4: Legibilidade:      Ausencia de comentarios esclarecendo razões das opções de implementação

#  CODIGO

def NormalizaLista ( ListaTrechos )   :
    ListaNormalizada = [ ]
    InclusaoOrdenados = sorted  (   ListaTrechos    ,   key=lambda Par  : Par   [   0   ]   ) 
    for ProximoTrecho in InclusaoOrdenados  :                                                 
            if not ListaNormalizada  :                                                        
                ListaNormalizada.append  (   ProximoTrecho )                                  
            else    :                                                                                
                Anterior = ListaNormalizada    [   -   1   ]                                         
                if ProximoTrecho  [   0   ] <= Anterior [   1   ]   :                                 
                    LimitePosterior = max   (   Anterior  [   1   ]   , ProximoTrecho   [   1   ]   ) 
                    ListaNormalizada [   -   1   ] = (   Anterior  [   0   ]   , LimitePosterior   )  
                else    :
                    ListaNormalizada.append  (   ProximoTrecho )                                      
    return ListaNormalizada
