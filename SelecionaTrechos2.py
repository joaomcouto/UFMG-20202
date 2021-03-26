# Este programa python recebe como contribuicoes para a publicacao de um video listas com trechos de intereSse e trechos que devem ser vetados. Cada trecho é representado pelos indices dos frames de inicio e fim
# As contribuicoes vem de diversas fontes, e portanto podem estar desordenadas ou sobrepostas
# Seu objetivo e gerar uma lista de trechos a publicar, ordenada, sem sobreposicoes, cobrindo apenas os trechos de interesse mas nao os trechos vetados

# Revisao 1: Legibilidade:      Nomeclatura orientada a tipos de dados dificulta entendimento do codigo, prejudicando manutenção e evolução
# Revisao 2: Sintaxe:           Comando "return" nao tem a mesma identacao da definicao da funcao, "def" e sim a dos comandos da funcao que terminam em sua declaração

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
