# Este programa python recebe como contribuicoes para a publicacao de um video listas com trechos de intereSse e trechos que devem ser vetados. Cada trecho é representado pelos indices dos frames de inicio e fim
# As contribuicoes vem de diversas fontes, e portanto podem estar desordenadas ou sobrepostas
# Seu objetivo e gerar uma lista de trechos a publicar, ordenada, sem sobreposicoes, cobrindo apenas os trechos de interesse mas nao os trechos vetados

# Revisao 1: Legibilidade:      Nomeclatura orientada a tipos de dados dificulta entendimento do codigo, prejudicando manutenção e evolução
# Revisao 2: Sintaxe:           Comando "return" nao tem a mesma identacao da definicao da funcao, "def" e sim a dos comandos da funcao que terminam em sua declaração
# Revisao 3: Bug:               O programa tenta percorrer retirar elementos mesmo de listas vazias
# Revisao 4: Logica/Correção:   Na repetição da função Removeintervalos, espera-se que a variavel de controle do loop varie necessariamente a cada iteracao e em cada iteraçao tenha um tratammento adequado.
#                               O exame dos blocos if mostra duas atribuições ao "ProximoCandidato" dentro de uma mesma iteração.
#                               Sintomaticamente, testes apresentam resultados com trechos vetados
# Revisao 5: Legibilidade:      Nomeclatura com nomes "burros", não semânticos, torna dificil entender e, por consequencia manter e evoluir o codigo
# Revisao 6: Legibilidade:      Ausencia de comentarios esclarecendo razões das opções de implementação

#  CODIGO

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
