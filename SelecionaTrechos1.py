# Este programa python recebe como contribuicoes para a publicacao de um video listas com trechos de intereSse e trechos que devem ser vetados. Cada trecho é representado pelos indices dos frames de inicio e fim
# As contribuicoes vem de diversas fontes, e portanto podem estar desordenadas ou sobrepostas
# Seu objetivo e gerar uma lista de trechos a publicar, ordenada, sem sobreposicoes, cobrindo apenas os trechos de interesse mas nao os trechos vetados

# Revisao 1: Legibilidade:      Nomeclatura orientada a tipos de dados dificulta entendimento do codigo, prejudicando manutenção e evolução


#  CODIGO

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
