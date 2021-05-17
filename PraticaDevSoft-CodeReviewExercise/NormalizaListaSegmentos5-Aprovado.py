# Este programa python recebe uma lista de pares ordenados definindo trechos de um pequeno video, por exemplo
# [ (   49   , 80 )   , ( 600  , 1013   )   , ( 42   , 78 ) , ( 449 , 557 )  , ( 852  , 961    ) , ( 111  , 119   )   , ( 77   , 139    ) ].
# Cada par é da forma (frame inicial, frame final). Observe que os trechos estao desordenados e se sobrepõe.

#O objetivo deste código é gerar um nova lista que contemple todos os trechos da lista, em ordem e sem sobreposição.

#Assim uma lista de entrada [( 49 , 80 )  e ( 42 , 78 )] retorna a saída [(42,80)]

# Revisao 1: Sintaxe:           Comando "return" nao tem a mesma identacao da definicao da funcao, "def" e sim a dos comandos da funcao que terminam em sua declaração
# Revisao 2: Legibilidade:      Nomeclatura baseada a tipos de dados, sem referencia a funcao de cada dado, dificulta entendimento do codigo, prejudicando manutenção e evolução
# Revisao 3: Logica/Correção:   A verificacao da relacao entre os trechos ocorre corretamente, porém na ordem que informados. Sobreposicoes entre trechos que  estiveremm disjuntos não são detectadas
# Revisao 4: Legibilidade:      Ausencia de comentarios esclarecendo razões das opções de implementação
# Revisao 5: Aprovado

#  CODIGO

def NormalizaLista ( ListaTrechos )   :
    ListaNormalizada = [ ]
    InclusaoOrdenados = sorted  (   ListaTrechos    ,   key=lambda Par  : Par   [   0   ]   )   # Ordena trechos pelo frame de inicio
    for ProximoTrecho in InclusaoOrdenados  :                                                   # Carrega cada trecho ordenado como proximo trecho candidato
            if not ListaNormalizada  :                                                          # Se lista normalizada estiver vazia, na primeira passagem
                ListaNormalizada.append  (   ProximoTrecho )                                    # inicializa a lista normalizada com proximo trecho, 
            else    :                                                                                  # Senão, depois da inicialização
                Anterior = ListaNormalizada    [   -   1   ]                                           # Copia temporaria do trecho anterior
                if ProximoTrecho  [   0   ] <= Anterior [   1   ]   :                                  # Verifica se o inicio do proximo trecho é anterior ou o proprio fim do trecho anterior
                    LimitePosterior = max   (   Anterior  [   1   ]   , ProximoTrecho   [   1   ]   )  # Se sim, atualiza o fim do trecho consolidado o fim fim do proximo, se este for posterior
                    ListaNormalizada [   -   1   ] = (   Anterior  [   0   ]   , LimitePosterior   )   # Substitui o trecho anterior pelo trecho consolidado
                else    :
                    ListaNormalizada.append  (   ProximoTrecho )                                       # Se o proximo trecho inicia após o fim do anteerio carregado, acrescenta o proximom a lista normalizada
    return ListaNormalizada



#Teste para verificar que o aluno fez a correção da revisão 3 
TrechosDeInteresse =  [ (   49   , 80 )   , ( 600  , 1013   )   , ( 42   , 78 ) , ( 449 , 557 )  , ( 852  , 961    ) , ( 111  , 119   )   , ( 77   , 139    ) ]
InteresseConsolidado    = NormalizaLista    (   TrechosDeInteresse  )
print   (   "Lista de trechos de interesse informada    : {}".format    (   TrechosDeInteresse     )   )
print   (   "Lista normmalizada de trechos de interesse : {}".format    (   InteresseConsolidado     )   )
TrechosDeInteresse =  [   (  38 , 50 ) , (   10  , 20    )  , ( 71 , 77 )  ]
InteresseConsolidado    = NormalizaLista    (   TrechosDeInteresse  )
print   (   "Lista de trechos de interesse informada    : {}".format    (   TrechosDeInteresse     )   )
print   (   "Lista normmalizada de trechos de interesse : {}".format    (   InteresseConsolidado     )   )
TrechosDeInteresse =  [   ]
InteresseConsolidado    = NormalizaLista    (   TrechosDeInteresse  )
print   (   "Lista de trechos de interesse informada    : {}".format    (   TrechosDeInteresse     )   )
print   (   "Lista normmalizada de trechos de interesse : {}".format    (   InteresseConsolidado     )   )

