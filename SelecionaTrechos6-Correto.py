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
    InclusaoOrdenados = sorted  (   ListaTrechos    ,   key=lambda Par  : Par   [   0   ]   )   # Ordena trechos pelo frame de inicio
    for ProximoTrecho in InclusaoOrdenados  :                                                   # Le proximo trecho candidato
            if not ListaNormalizada  :
                ListaNormalizada.append  (   ProximoTrecho )                                    # inicializa com proximo trecho
            else    :
                Anterior = ListaNormalizada    [   -   1   ]                                      # Analisa trecho anterior
                if ProximoTrecho  [   0   ] <= Anterior [   1   ]   :                                   
                    LimitePosterior = max   (   Anterior  [   1   ]   , ProximoTrecho   [   1   ]   )  # Pela ordenacao Anterior [   0   ] eh menor que ProximoTrecho  [   0   ]
                    ListaNormalizada [   -   1   ] = (   Anterior  [   0   ]   , LimitePosterior   )  # substitui por intervalo consolidada
                else    :
                    ListaNormalizada.append  (   ProximoTrecho )
    return ListaNormalizada
    
def RemoveIntervalos (   InclusaoConsolidado    ,   ExclusaoConsolidado )   :
    ListaPublicacao = [ ]
    ProximaExclusao = ()
    if ExclusaoConsolidado :
        ProximaExclusao = ExclusaoConsolidado . pop ( 0 )
    ProximoCandidato = ()
    if InclusaoConsolidado :
        ProximoCandidato = InclusaoConsolidado . pop ( 0 )
    while ProximoCandidato :
        if ( not ProximaExclusao ) :
            ListaPublicacao . append ( ProximoCandidato )       # Fim exclusões" )                     
        elif ( ProximoCandidato [ 1 ] < ProximaExclusao [ 0 ] ) :    # Proximo candidato termina antes que a proxima exclusao comece" ) 
            ListaPublicacao . append ( ProximoCandidato )
        elif ProximoCandidato [ 1 ] <= ProximaExclusao [ 1 ] :
            if ProximoCandidato [ 0 ] < ProximaExclusao [ 0 ] :  # Proximo candidato termina dentro da proxima exclusao" ) 
                ListaPublicacao . append ( ( ProximoCandidato[0] , ProximaExclusao [ 0 ] - 1 ) )
        else :
            if ProximoCandidato [ 0 ] < ProximaExclusao [ 0 ] :
                ListaPublicacao . append  ( ( ProximoCandidato[0]          ,   ProximaExclusao [ 0 ] - 1 ) )  # Proximo candidato termina depois da proxima exclusao mas começa antes" )
                ProximoCandidato = ( ProximaExclusao[1] + 1    ,   ProximoCandidato [ 1 ]   )
                continue
            elif ProximoCandidato [ 0 ] <= ProximaExclusao [ 1 ] :
                ListaPublicacao . append  ( ( ProximaExclusao[1] + 1    ,   ProximoCandidato [ 1 ]       ) ) # Proximo candidato termina depois da proxima exclusao mas commeça dentro" )
            else :
                ProximaExclusao = ()                     # Proximo candidato termina depois da proxima exclusao e comeca depois " )
                if ExclusaoConsolidado :
                    ProximaExclusao = ExclusaoConsolidado . pop ( 0 )
                continue
        ProximoCandidato = ()
        if InclusaoConsolidado :
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

#########  TESTE  ################################

TrechosDeInteresse = [  (   4   , 8 )   , ( 60  , 101   )   , ( 4   , 7 ) , ( 44 , 55 )  , ( 85  , 91    ) , ( 11  , 11    )   , ( 7   , 13    )   ]
TrechosCensurados = [   (  38 , 50 ) , (   10  , 20    )  , ( 71 , 77 )  ]
PreparaPublicacao ( TrechosDeInteresse , TrechosCensurados )
TrechosCensurados = [    ]
PreparaPublicacao ( TrechosDeInteresse , TrechosCensurados )
TrechosDeInteresse = [  ]
TrechosCensurados = [   (  38 , 50 ) , (   10  , 20    )  , ( 71 , 77 )  ]
PreparaPublicacao ( TrechosDeInteresse , TrechosCensurados )
TrechosCensurados = [ ]
TrechosDeInteresse = [  ]
PreparaPublicacao ( TrechosDeInteresse , TrechosCensurados )
