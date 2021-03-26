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
    
def RemoveIntervalos (   InclusaoConsolidado    ,   ExclusaoConsolidado )   :
    ListaPublicacao = [ ]
    ProximaExclusao = ()
    ProximaExclusao = ExclusaoConsolidado . pop ( 0 )
    ProximoCandidato = ()
    ProximoCandidato = InclusaoConsolidado . pop ( 0 )
    while ProximoCandidato :
        if ( not ProximaExclusao ) :
            ListaPublicacao . append ( ProximoCandidato )      
        elif ( ProximoCandidato [ 1 ] < ProximaExclusao [ 0 ] ) : 
            ListaPublicacao . append ( ProximoCandidato )
        elif ProximoCandidato [ 1 ] <= ProximaExclusao [ 1 ] :
            if ProximoCandidato [ 0 ] < ProximaExclusao [ 0 ] :  
                ListaPublicacao . append ( ( ProximoCandidato[0] , ProximaExclusao [ 0 ] - 1 ) )
        else :
            if ProximoCandidato [ 0 ] < ProximaExclusao [ 0 ] :
                ListaPublicacao . append  ( ( ProximoCandidato[0]          ,   ProximaExclusao [ 0 ] - 1 ) ) 
                ProximoCandidato = ( ProximaExclusao[1] + 1    ,   ProximoCandidato [ 1 ]   )            #  visita descartada sem tratammento
            elif ProximoCandidato [ 0 ] <= ProximaExclusao [ 1 ] :
                ListaPublicacao . append  ( ( ProximaExclusao[1] + 1    ,   ProximoCandidato [ 1 ]       ) ) 
            else :
                ProximaExclusao = ()                    
                ProximaExclusao = ExclusaoConsolidado . pop ( 0 )                               #  visita descartada sem tratammento
        ProximoCandidato = ()
        ProximoCandidato = InclusaoConsolidado . pop ( 0 )
return ListaPublicacao
    
def PreparaPublicacao ( ListaInteresse , ListaVeto )    :
    print   ( "." )
    InteresseConsolidado    = NormalizaLista    (   ListaInteresse  )
    print   (   "Lista normmalizada de trechos de interesse : {}".format    (   InteresseConsolidado     )   )
    VetadosConsolidados     = NormalizaLista    (   ListaVeto       )
    print   (   "Lista normalizada de trechos vetados       : {}".format    (   VetadosConsolidados     )   )
    TrechosPublicados       = RemoveIntervalos  (   InteresseConsolidado , VetadosConsolidados )
    print   (   "Trechos para publicacao                 : {}".format    (   TrechosPublicados     )   )
    print   ( "." )
return
