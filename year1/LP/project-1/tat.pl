% Jaime Ribeiro Barrancos 1109262
:- use_module(library(clpfd)).
:- set_prolog_flag(answer_write_options,[max_depth(0)]).
:- ['puzzlesAcampar.pl'].



/*----------------------------------------------------------------------

                        Predicados de consulta

----------------------------------------------------------------------*/

/* 
vizinhanca/2 e verdade se Vizinhanca e uma lista ordenada de cima 
    para baixo e da esquerda para a direita, sem elementos repetidos, 
    com as coordenadas das posicoes imediatamente acima, imediatamente 
    a esquerda, imediatamente a direita e imediatamente abaixo da 
    coordenada (L, C).
*/
vizinhanca((L, C), Vizinhanca) :-
    X1 is C - 1, X2 is C + 1, Y1 is L - 1, Y2 is L + 1,
    Vizinhanca = [(Y1, C), (L, X1), (L, X2), (Y2, C)].

/* 
vizinhancaAlargada/2 e verdade se VizinhancaAlargada e uma lista 
    ordenada de cima para baixo e da esquerda para a direita, sem 
    elementos repetidos, com as coordenadas anteriores e ainda as 
    diagonais da coordenada (L, C).
*/
vizinhancaAlargada((L, C), Vizinhanca) :-
    X1 is C - 1, X2 is C + 1, Y1 is L - 1, Y2 is L + 1,
    Vizinhanca = [(Y1, X1), (Y1, C), (Y1, X2), (L, X1), (L, X2), (Y2, X1), (Y2, C), (Y2, X2)].

/*
todasCelulas/2 e verdade se TodasCelulas e uma lista ordenada de cima 
    para baixo e da esquerda para a direita, sem elementos repetidos, com 
    todas as coordenadas do tabuleiro.
*/
todasCelulas(Tabuleiro, TodasCelulas) :-
    findall(
        (Y,X), 
        (nth1(Y, Tabuleiro, Linha), nth1(X, Linha, _)), 
        TodasCelulas).

/*
todasCelulas/2 e verdade se TodasCelulas e uma lista ordenada de cima para 
    baixo e da esquerda para a direita, sem elementos repetidos, com todas as 
    coordenadas do tabuleiro Tabuleiro em que existe um objecto do tipo Objecto.
*/
todasCelulas(Tabuleiro, TodasCelulas, Objeto) :-
    findall(
        (Y,X), 
        (nth1(Y, Tabuleiro, Linha),
        nth1(X, Linha, Celula),
        (nonvar(Objeto), Celula == Objeto ; var(Objeto), var(Celula))
        ), TodasCelulas).

/*
contagem/3 e verdade se Lista tem Contagem numero de Objetos, isto e, se
        o Objeto se encontra na Linha N vezes em que N e a Contagem.
*/
contagem(Objeto, Linha, Contagem) :-
    findall(
        Celula,
        (member(Celula, Linha),
        (nonvar(Objeto), Celula == Objeto ; var(Objeto), var(Celula))),
        ObjetosNaLinha),
    length(ObjetosNaLinha, Contagem).

/*
calculaObjectosTabuleiro/4 e verdade se Tabuleiro for um tabuleiro, Objecto 
    for o tipo de objecto que se procura, e ContagemLinhas e ContagemColunas forem, 
    respectivamente, listas com o numero desses objectos por linha e por coluna.
*/
calculaObjectosTabuleiro(Tabuleiro, ContagemLinhas, ContagemColunas, Objeto) :-
    maplist( 
        contagem(Objeto),
        Tabuleiro,
        ContagemLinhas
        ),
    transpose(Tabuleiro, TabuleiroTransposto),
    maplist( 
        contagem(Objeto),
        TabuleiroTransposto,
        ContagemColunas
        ).

/*
objetoNaPos/3 e verdade se o Objeto estiver na posicao (Y, X) do Tabuleiro.
*/
objetoNaPos(Tabuleiro, (Y, X), Objeto) :-
    nth1(Y, Tabuleiro, Linha),
    nth1(X, Linha, Objeto).

/*
celulaVazia/2 e verdade se Tabuleiro for um tabuleiro que nao tem nada ou tem 
    relva nas coordenadas (L, C). Se as coordenadas nao fizerem parte do tabuleiro, 
    o predicado nao deve falhar.
*/
celulaVazia(Tabuleiro, (L, C)) :-
    objetoNaPos(Tabuleiro, (L, C), Objeto),
    var(Objeto).



/*----------------------------------------------------------------------

                    Predicados de inserir tendas e relva

----------------------------------------------------------------------*/

/*
insereObjectoCelula/3 e verdade se Tabuleiro e um tabuleiro e (L, C) sao as coordenadas 
    para se inserir o objecto TendaOuRelva.
*/
insereObjectoCelula(Tabuleiro, TendaOuRelva, (L, C)) :-
    objetoNaPos(Tabuleiro, (L, C), Objeto),
    auxInsere(Objeto, TendaOuRelva).

auxInsere(Objeto, _) :-
    (Objeto == t; Objeto == r; Objeto == a).
auxInsere(Objeto, TendaOuRelva) :-
    Objeto = TendaOuRelva.


/*
insereAux/4 e verdade se o tabuleiro, na posicao, L, C estiver com r, a, 
    t ou _. Sendo que unifica caso seja _.
*/
insereAux(Tabuleiro, TendaOuRelva, L, C) :-
    insereObjectoCelula(Tabuleiro, TendaOuRelva, (L, C)).

/*
insereObjectoEntrePosicoes/4 e verdade se Tabuleiro e um tabuleiro, e (L, C1) 
    e (L, C2) sao as coordenadas, na Linha L, entre as quais (incluindo) se insere 
    o objecto TendaOuRelva.
*/
insereObjectoEntrePosicoes(Tabuleiro, TendaOuRelva, (L, C1), (L, C2)) :-
    findall(C, between(C1, C2, C), Elementos),
    maplist(
        insereAux(Tabuleiro, TendaOuRelva, L), 
        Elementos).



/*----------------------------------------------------------------------

                        Predicados de estrategias

----------------------------------------------------------------------*/

/*
comparaInsereTendas/3 e verdade quando as quantidades de tendas desejadas por 
    linha/coluna sao as atuais e existe relva de modo a completar a linha/coluna.
*/
comparaInsereTendas(Tabuleiro, TendasDesejadasLinha, Indice):-

    nth1(Indice, Tabuleiro, Linha),

    % conta os t na linha
    findall(X, (member(X, Linha), X == t), Tendas),
    length(Tendas, QtdTendas),

    insereRelvaAux(Tabuleiro, TendasDesejadasLinha, QtdTendas, Indice).

/*
insereRelvaAux/4 e verdade se as quantidades de tendas desejadas por 
    linha/coluna sao as atuais e a linha/coluna tem relva nas restantes
    celulas ou se as quantidades nao sao as desejadas.
*/
insereRelvaAux(Tabuleiro, TendasDesejadasLinha, QtdTendas, Indice) :-
    % se sao iguais insere relva no resto
    TendasDesejadasLinha == QtdTendas,
    length(Tabuleiro, Tamanho),
    insereObjectoEntrePosicoes(Tabuleiro, r, (Indice, 1), (Indice, Tamanho)).

insereRelvaAux(_,TendasDesejadasLinha, QtdTendas,_) :-
    % se forem diferentes nao fazer nada
    TendasDesejadasLinha \== QtdTendas.

/*
relva/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, tem 
    relva em todas as linhas/colunas cujo numero de tendas ja atingiu o numero de 
    tendas possivel nessas linhas/colunas.
*/
relva(Puzzle) :-

    Puzzle = (Tabuleiro, QtdsTendasLinhaDesej, QtdsTendasColDesej),

    % cria lista com indices para percorrer
    length(Tabuleiro, Tamanho),
    findall(Indice, between(1, Tamanho, Indice), Indices),

    % por cada linha, caso o numero de tendas seja o desejado
    % entao unifica relva onde possivel (pode haver arvore)
    maplist(
        comparaInsereTendas(Tabuleiro),
        QtdsTendasLinhaDesej,
        Indices),
    transpose(Tabuleiro, NovoTabuleiro),
    maplist(
        comparaInsereTendas(NovoTabuleiro),
        QtdsTendasColDesej,
        Indices),
    transpose(NovoTabuleiro, Tabuleiro).

/*
inacessiveis/1 e verdade se Tabuleiro e um tabuleiro que, apos a aplicacao do 
    predicado, tem relva em todas as posicoes inacessiveis.
*/
inacessiveis(Tabuleiro) :-
    % todas as arvores
    todasCelulas(Tabuleiro, TodasArvores, a),

    % quais sao acessiveis (adjacentes a arvores)
    maplist(
        vizinhanca,
        TodasArvores,
        AcessiveisUnflat
    ),

    % transformar numa lista unica
    flatten(AcessiveisUnflat, Acessiveis),
    todasCelulas(Tabuleiro, TodasCelulas),

    % quando sao membro de todas as celulas e nao das acessiveis 
    % sao inacessiveis
    findall(
        Celula,
        (member(Celula, TodasCelulas), 
        \+ member(Celula, Acessiveis)),
        Inacessiveis),

    % insere relva nas inacessiveis
    maplist(
        insereObjectoCelula(Tabuleiro, r),
        Inacessiveis).

/*
posicoesLivresAux/3 e verdade se Tabuleiro, apos a aplicacao do predicado, 
    tem tendas na Linha onde faltava colocar N tendas e que tinha exatamente N 
    posicoes livres.
*/
posicoesLivresAux(Tabuleiro, TendasDesejadasLinha, Indice):-
    nth1(Indice, Tabuleiro, Linha),

    % conta tendas
    findall(X, (member(X, Linha), (X == t)), Tendas),
    length(Tendas, QtdTendas),

    % conta posicoes livres
    findall(X, (member(X, Linha), (var(X))), Vazios),
    length(Vazios, PosicoesLivres),

    insereTendaAux(Tabuleiro, PosicoesLivres, QtdTendas, TendasDesejadasLinha, Indice).

/*
insereTendaAux/5 e verdade se as tendas forem inseridas nas posicoes livres do Tabuleiro
    na linha onde a quantidade de tendas que faltam seja a subtracao da quantidade das 
    tendas desejadas com a quantidade das posicoes livres, isto e:
    QtdTendas == TendasDesejadasLinha - PosicoesLivres.
*/
insereTendaAux(Tabuleiro, PosicoesLivres, QtdTendas, TendasDesejadasLinha, Indice) :-
    length(Tabuleiro, Tamanho),

    % se sao iguais insere tendas onde possivel
    TendasDesejadasLinha is QtdTendas + PosicoesLivres,
    
    insereObjectoEntrePosicoes(Tabuleiro, t, (Indice, 1), (Indice, Tamanho)).

insereTendaAux(_,PosicoesLivres, QtdTendas,TendasDesejadasLinha,_) :-
    % se forem diferentes nao fazer nada
    \+ (TendasDesejadasLinha is QtdTendas + PosicoesLivres).
    
/*
aproveita/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, 
    tem tendas em todas as linhas e colunas as quais faltavam colocar X tendas e que 
    tinham exatamente X posicoes livres.
*/
aproveita(Puzzle) :-
    Puzzle = (Tabuleiro, QtdsTendasLinhaDesej, QtdsTendasColDesej),

    % cria lista com indices para percorrer
    length(Tabuleiro, Tamanho),
    findall(Indice, between(1, Tamanho, Indice), Indices),

    % por cada linha, caso o numero de posicoes livres seja 
    % o desejado entao unifica tendas nas posicoes livres
    maplist(
        posicoesLivresAux(Tabuleiro),
        QtdsTendasLinhaDesej,
        Indices),
    transpose(Tabuleiro, NovoTabuleiro),
    maplist(
        posicoesLivresAux(NovoTabuleiro),
        QtdsTendasColDesej,
        Indices),
    transpose(NovoTabuleiro, Tabuleiro).

/*
auxTentaInserirRelva/2 e verdade se o objeto for inserido na celula (L, C)
    do tabuleiro ou nao, logo e sempre verdade (nao falha).
*/
auxTentaInserirRelva(Tabuleiro, (L, C)) :-
    (insereObjectoCelula(Tabuleiro, r, (L, C)) ; true).

/*
limpaVizinhancas/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, 
    tem relva em todas as posicoes a volta de uma tenda.
*/
limpaVizinhancas(Puzzle) :-
    Puzzle = (Tabuleiro, _, _),
    todasCelulas(Tabuleiro, Tendas, t),

    maplist(
        vizinhancaAlargada,
        Tendas,
        Vizinhancas
    ),
    flatten(Vizinhancas, CoordenadasALimpar),

    maplist(
        auxTentaInserirRelva(Tabuleiro),
        CoordenadasALimpar).

/*
auxTendaNaVizinhanca/2 e verdade se a vizinhanca da Arvore tem 1 ou mais tendas.
*/
auxTendaNaVizinhanca(Tabuleiro, Vizinhanca) :-
    todasCelulas(Tabuleiro, TodasTendas, t),
    findall(Tenda, (member(Tenda, TodasTendas), member(Tenda, Vizinhanca)), TendasNaVizinhanca),
    length(TendasNaVizinhanca, Length),
    Length \== 0.

/*
auxVizinhancaCom1Elemento/2 e verdade se Tabuleiro tem na vizinhanca da Arvore 
    apenas 1 celula vazia na qual se insere uma tenda.
*/
auxVizinhancaCom1Elemento(Tabuleiro, Arvore) :-
    vizinhanca(Arvore, Vizinhanca),
    findall(
        Adjacente, 
        (member(Adjacente, Vizinhanca), 
        \+ auxTendaNaVizinhanca(Tabuleiro, Vizinhanca),
        celulaVazia(Tabuleiro, Adjacente)),
        VizinhancasLivres),
    ((length(VizinhancasLivres, 1), member(UnicoLivre, VizinhancasLivres),
    insereObjectoCelula(Tabuleiro, t, UnicoLivre)) ;  true).

/*
unicaHipotese/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, 
    todas as arvores que tinham apenas uma posicao livre na sua vizinhanca que lhes 
    permitia ficar ligadas a uma tenda, tem agora uma tenda nessa posicao.
*/
unicaHipotese(Puzzle) :-
    Puzzle = (Tabuleiro, _, _),
    todasCelulas(Tabuleiro, Arvores, a),

    maplist(
        auxVizinhancaCom1Elemento(Tabuleiro),
        Arvores).



/*----------------------------------------------------------------------

                    Predicados de tentativa e erro

----------------------------------------------------------------------*/

/*
valida/2 e verdade se LArv e LTen sao listas com todas as coordenadas em que 
    existem, respectivamente, arvores e tendas, e e avaliado para verdade se for 
    possivel estabelecer uma relacao em que existe uma e uma unica tenda para cada 
    arvore nas suas vizinhancas (bijecao).
*/
valida(Arvores, Tendas) :-
    length(Arvores, N),
    length(Tendas, N),
    auxTendaPorArvore(Arvores, Tendas, _).

/*
auxTendaPorArvore/3 e verdade quando cada arvore tem uma tenda diretamente
    associada a sua vizinhanca.
*/
auxTendaPorArvore([], _, []).
auxTendaPorArvore([Arvore|RestoArvores], Tendas, [Tenda|RestoTendas]) :-
    % se 2 tendas pertencem a mesma arvore tem de haver uma tenda sozinha
    vizinhanca(Arvore, Vizinhanca),
    member(Tenda, Vizinhanca),
    member(Tenda, Tendas),
    auxTendaPorArvore(RestoArvores, Tendas, RestoTendas),
    % adiciona Tenda a RestoTendas quando comecar o backtracking
    \+ member(Tenda, RestoTendas).

/*
resolve/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, 
    fica resolvido.
*/
resolve(Puzzle) :-
    Puzzle = (Tabuleiro, _, _),
    inacessiveis(Tabuleiro),

    auxResolve(Puzzle).

/*
validaFinal/1 e verdade se Puzzle e um puzzle resolvido, isto e, nao ha celulas
    livres, as quantidades de tendas desejadas por linha/coluna corresponde
    a quantidade atual de tendas por linha/coluna e e um puzzle valido.
*/
validaFinal(Puzzle) :-
    Puzzle = (Tabuleiro, QtdsTendasLinhaDesej, QtdsTendasColDesej),
    calculaObjectosTabuleiro(Tabuleiro, QtdsTendasLinhaDesej, QtdsTendasColDesej, t),

    % nao pode haver celulas livres
    todasCelulas(Tabuleiro, [], _),

    todasCelulas(Tabuleiro, Arvores, a),
    todasCelulas(Tabuleiro, Tendas, t),

    valida(Arvores, Tendas).

/*
puzzleDiferentes/2 e verdade se Puzzle e diferente de Puzzle2 (apenas nas celulas
    vazias).
*/
puzzleDiferentes(Puzzle, Puzzle2):-
    Puzzle = (Tabuleiro, _, _),
    Puzzle2 = (Tabuleiro2, _, _),
    todasCelulas(Tabuleiro, TodasVazias1, _),
    todasCelulas(Tabuleiro2, TodasVazias2, _),
    TodasVazias1 \== TodasVazias2.

/*
aplicaPredicados/1 e verdade se Puzzle e um puzzle com a aplicacao dos predicados relva, 
    aproveita, unicaHipotese e limpaVizinhancas.
*/
aplicaPredicados(Puzzle) :-
    relva(Puzzle),
    aproveita(Puzzle),
    unicaHipotese(Puzzle),
    limpaVizinhancas(Puzzle),!.

/*
auxResolve/1 e verdade se Puzzle e um puzzle que, apos a aplicacao do predicado, 
    fica resolvido.
*/
% caso terminal de tabuleiro estar preenchido
auxResolve(Puzzle) :-
    Puzzle = (Tabuleiro, _, _),
    todasCelulas(Tabuleiro, [], _).

% aplica predicados ate nao dar mais
auxResolve(Puzzle) :-
    copy_term(Puzzle, Copia),

    % aplica todos predicados
    aplicaPredicados(Puzzle),
    puzzleDiferentes(Puzzle, Copia),!,

    auxResolve(Puzzle).

% coloca tenda
auxResolve(Puzzle) :-
    Puzzle = (Tabuleiro, _, _),

    % encontra uma tenda
    todasCelulas(Tabuleiro, Vazias, _),
    member(TendaAgora, Vazias),

    % coloca a tenda
    insereObjectoCelula(Tabuleiro, t, TendaAgora),

    auxResolve(Puzzle),

    % quando acabar tem de ser um puzzle resolvido
    validaFinal(Puzzle).