# Este código é uma função de uma plataforma de edição de vídeo colobarativa. 
# No contexto da edição de um vídeo especifico o administrador envia duas listas:
            #Uma lista contendo tuplas de trechos que seus colaboradores mais gostaram
            #Uma lista contendo tuplas de trechos que seus colaboradores acham que devem ser removidos

# Cada trecho é representado por uma tupla (indice dos frame de inicio,indice do frame final)

# Ambas as listas de entrada podem estar desordenadas e com trechos com sobreposições

# Assim, a funcão deste este programa python é receber essas duas listas e retornar uma lista final de trechos
# Essa lista final é construida de tal forma que
     # Contemple todos os trechos da primeira lista (trechos mais gostados) desde que, 
     # não estejam dentro da lista de trechos a serem removidos
# Ou seja, o programa 
    # 1 - Ordena e elimina sobreposições (fazendo merges de trechos) de cada lista e depois,
    # 2 - elimina da lista de inclusão todos os trechos que estejam na lista de exclusão

# Revisao 1: Legibilidade:      Variaveis com nomes não semânticos, torna dificil entender e, por consequencia manter e evoluir o codigo

# Revisao 2: Sintaxe:           Comando "return" das funções nao tem a mesma identacao da definicao do "def" delas

# Revisao 3: Bug:               O programa tenta percorrer retirar elementos mesmo de listas vazias

# Revisao 4: Logica/Correção:   Na repetição da função Removeintervalos, espera-se que a variavel de controle do loop varie necessariamente a cada iteracao e em cada iteraçao tenha um tratammento adequado.
#                               O exame dos blocos if mostra duas atribuições ao "ProximoCandidato" dentro de uma mesma iteração.
#                               Sintomaticamente, testes apresentam resultados com trechos vetados

# Revisao 5: Legibilidade:      Ausencia de comentarios esclarecendo razões das opções de implementação

def NormalizaLista ( Lista1 )   :
    Lista2 = [ ]
    Lista3 = sorted  (   Lista1    ,   key=lambda Par  : Par   [   0   ]   ) 
    for Tupla1 in Lista3  :                                                 
            if not Lista2  :
                Lista2.append  (   Tupla1 )                                  
            else    :
                Tupla2 = Lista2    [   -   1   ]                                  
                if Tupla1  [   0   ] <= Tupla2 [   1   ]   :                                   
                    Frame1 = max   (   Tupla2  [   1   ]   , Tupla1   [   1   ]   ) 
                    Lista2 [   -   1   ] = (   Tupla2  [   0   ]   , Frame1   ) 
                else    :
                    Lista2.append  (   Tupla1 )
return Lista2
    
def RemoveIntervalos (   Lista4    ,   Lista5 )   :
    Lista6 = [ ]
    Tupla3 = ()
    Tupla3 = Lista5 . pop ( 0 )
    Tupla4 = ()
    Tupla4 = Lista4 . pop ( 0 )
    while Tupla4 :
        if ( not Tupla3 ) :
            Lista6 . append ( Tupla4 )      
        elif ( Tupla4 [ 1 ] < Tupla3 [ 0 ] ) : 
            Lista6 . append ( Tupla4 )
        elif Tupla4 [ 1 ] <= Tupla3 [ 1 ] :
            if Tupla4 [ 0 ] < Tupla3 [ 0 ] :  
                Lista6 . append ( ( Tupla4[0] , Tupla3 [ 0 ] - 1 ) )
        else :
            if Tupla4 [ 0 ] < Tupla3 [ 0 ] :
                Lista6 . append  ( ( Tupla4[0]          ,   Tupla3 [ 0 ] - 1 ) ) 
                Tupla4 = ( Tupla3[1] + 1    ,   Tupla4 [ 1 ]   )            #  visita descartada sem tratammento
            elif Tupla4 [ 0 ] <= Tupla3 [ 1 ] :
                Lista6 . append  ( ( Tupla3[1] + 1    ,   Tupla4 [ 1 ]       ) ) 
            else :
                Tupla3 = ()                    
                Tupla3 = Lista5 . pop ( 0 )                               #  visita descartada sem tratammento
        Tupla4 = ()
        Tupla4 = Lista4 . pop ( 0 )
return Lista6
    
def PreparaPublicacao ( Lista7 , Lista8 )    :
    print   ( "." )
    InteresseConsolidado    = NormalizaLista    (   Lista7  )
    print   (   "Lista normmalizada de trechos de interesse : {}".format    (   InteresseConsolidado     )   )
    VetadosConsolidados     = NormalizaLista    (   Lista8       )
    print   (   "Lista normalizada de trechos vetados       : {}".format    (   VetadosConsolidados     )   )
    TrechosPublicados       = RemoveIntervalos  (   InteresseConsolidado , VetadosConsolidados )
    print   (   "Trechos para publicacao                 : {}".format    (   TrechosPublicados     )   )
    print   ( "." )
return
