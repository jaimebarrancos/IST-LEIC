###########################
# Jaime Ribeiro Barrancos #
###########################
# ----------------------- #
# ist1109262
# 23/24
# projeto: GO
# ----------------------- #


##################################################
# Operações de baixo nível para interseções      #
##################################################


def columnToNum(letter): # starts at 0
    """
    Recebe uma letra e devolve o index correspondente a essa letra no abcedário.
    """
    letterOrd = ord(letter)
    return letterOrd - 64

def obtem_col(inter):
    """
    Recebe uma interseção e devolve a coluna representada por uma letra que é o seu primeiro elemento.
    """
    return inter[0]

def obtem_lin(inter):
    """
    Recebe uma interseção e devolve a linha representada por um numero que é o seu segundo elemento.
    """
    return inter[1]

def eh_intersecao(inter):
    """
    Recebe um argumento de qualquer tipo e devolve True se o seu 
    argumento corresponde a uma interseção e False caso contrário, 
    sem nunca gerar erros.
    """
    
    # check is tuple with 2 elements
    if type(inter) != tuple or len(inter) != 2 :
        return False
    
    # check elements are appropriate
    if type(inter[1]) == int and type(inter[0]) == str and len(inter[0]) == 1 and 1 <= columnToNum(inter[0]) <= 19 and 1 <= inter[1] <= 19 :
        return True
    return False

def cria_intersecao(char, lin):
    """
    Recebe uma letra e um numero e devolve a interseção, caso seja válida.
    """
    inter = (char, lin)
    if not eh_intersecao(inter):
        raise ValueError('cria_intersecao: argumentos invalidos')
    return inter

def intersecoes_iguais(inter1, inter2):
    """
    Recebe duas interseções e averigua se são iguais.
    """
    # if each column and row are equal
    if obtem_col(inter1) == obtem_col(inter2) and obtem_lin(inter1) == obtem_lin(inter2):
        return True
    return False

def intersecao_para_str(inter):
    """
    Recebe uma interseção e devolve a sua representação em texto.
    """

    return obtem_col(inter) + str(obtem_lin(inter))
    
def str_para_intersecao(st):
    """
    Recebe texto que representa uma interseçãoe e retorna essa interseção.
    """
    #letra é apenas 1 digito, numero é o resto
    return (st[0], int(st[1:]))



##################################################
# Operações de alto nível para interseções       #
##################################################

def ordena_intersecoes(tup):
    """
    Recebe tuplo de interseções e retorna um tuplo com as intersecoes ordenadas .
    """

    def custom_key(inter):
        str_inter = intersecao_para_str(inter)
        col = columnToNum(str_inter[0])
        lin = int(str_inter[1:])
        return (lin, col)

    return tuple(sorted(tup, key=custom_key))

      
def obtem_intersecoes_adjacentes(inter, maxInter):
    """
    Recebe um território e uma interseção do território, e devolve o tuplo 
    formado pelas interseção válidas adjacentes da interseção em ordem de 
    leitura de um território.
    """

    strMax = intersecao_para_str(maxInter)
    maxLin =  int(strMax[1:])

    str_inter = intersecao_para_str(inter)
    col = columnToNum(str_inter[0])
    lin = int(str_inter[1:])

    # buscar intersecoes se tiverem entre os limites
    resultIntersections = ()
    if lin != 1 :
        resultIntersections += (cria_intersecao(chr(col + 64), lin - 1),)
    
    if col != 1:
        resultIntersections += (cria_intersecao(chr(col + 63), lin),)
    
    if maxLin != col:
        resultIntersections += (cria_intersecao(chr(col + 65), lin),)

    if maxLin != lin:
        resultIntersections += (cria_intersecao(chr(col + 64), lin + 1),)

    return ordena_intersecoes(resultIntersections)


##################################################
# Operações de baixo nível para pedra            #
##################################################

# branca - 1
# preta - 2
# neutra - 0
def eh_pedra(pedra):
    """
    Averigua se o que recebe é uma pedra.
    """
    if pedra == "1" or pedra == "2" or pedra == "3":
        return True
    return False

def cria_pedra_branca():
    """
    Devolve a pedra branca.
    """
    return "1"

def cria_pedra_preta():
    """
    Devolve a pedra preta.
    """
    return "2"

def cria_pedra_neutra():
    """
    Devolve a pedra neutra.
    """
    return "3"

def eh_pedra_branca(pedra):
    """
    Averigua se o que recebe é uma pedra branca.
    """
    if pedra == "1":
        return True
    return False

def eh_pedra_preta(pedra):
    """
    Averigua se o que recebe é uma pedra preta.
    """
    if pedra == "2":
        return True
    return False

def eh_pedra_neutra(pedra):
    """
    Averigua se o que recebe é uma neutra.
    """
    if pedra == "3":
        return True
    return False

def pedras_iguais(p1, p2):
    """
    Averigua as pedras que recebe são iguais.
    """
    if eh_pedra(p1) and eh_pedra(p2) and p1 == p2:
        return True
    return False

def pedra_para_str(pedra):
    """
    Transforma uma pedra para o seu formato em texto.
    """
    if eh_pedra_branca(pedra):
        return "O"
    if eh_pedra_preta(pedra):
        return "X"
    if eh_pedra_neutra(pedra):
        return "."


##################################################
# Operações de alto nível para pedra             #
##################################################

def eh_pedra_jogador(pedra):
    """
    Averigua se o que recebe é uma pedra de um jogador.
    """
    if eh_pedra(pedra) and not eh_pedra_neutra(pedra) :
        return True
    return False


##################################################
# Operações de baixo nível para goban            #
##################################################

def cria_goban_vazio(n):
    """
    Devolve um goban de n colunas e linhas vazio.
    """
    if (n != 9 and n != 13 and n != 19) or type(n) != int:
        raise ValueError("cria_goban_vazio: argumento invalido")
    
    goban = []
    line = []
    for x in range(1, n + 1, 1):
        for y in range(1, n + 1, 1):
            line.append("0")
        goban.append(line )
        line = []

    return goban

def cria_goban(n, interBrancas, interPretas):
    """
    Devolve um goban com n colunas e linhas. Com cada interseção dos tuplos 
    interBrancas e interPretas ocupadas com pedras dos jogadores brancos
    e pretos, respetivamente.
    """
    if type(interBrancas) != tuple or type(interPretas) != tuple:
        raise ValueError("cria_goban: argumentos invalidos")

    def auxAdicionaIntersecoes(goban, tup, tup2, pedra):
        # nao pode haver elementos repetidos nos dois tuplos e cada intersecao tem de ser valida
        for inter in tup:
            if not eh_intersecao_valida(goban, inter) or inter in tup2:
                raise ValueError("cria_goban: argumentos invalidos")
            
            str_inter = intersecao_para_str(inter)
            goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = pedra

    if (n != 9 and n != 13 and n != 19) or type(n) != int:
        raise ValueError("cria_goban: argumentos invalidos")
    
    goban = cria_goban_vazio(n)

    auxAdicionaIntersecoes(goban, interPretas, interBrancas, "2")
    auxAdicionaIntersecoes(goban, interBrancas, interPretas, "1")

    # nao pode haver elementos repetidos
    if len(set(interPretas)) != len(interPretas) or len(set(interBrancas)) != len(interBrancas):
        raise ValueError("cria_goban: argumentos invalidos")

    return goban

def cria_copia_goban(g):
    """
    Devolve a cópia do goban recebido.
    """
    gobanCopy = []
    for line in g:
        newLine = []
        for element in line:
            newLine.append(element)
        gobanCopy += [newLine]
    return gobanCopy

def obtem_ultima_intersecao(goban):
    """
    Devolve a última interseção do goban recebido.
    """

    count = 0
    # como numero de linhas = numero de colunas
    for line in goban:
        count += 1

    return cria_intersecao(chr(64 + count), count)

def obtem_pedra(goban, inter):
    """
    Devolve a pedra posicionada na interseção recebida, no goban recebido.
    """
    str_inter = intersecao_para_str(inter)
    pedraGoban = goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1]
    if pedraGoban == "2":
        return cria_pedra_preta()
    if pedraGoban == "1":
        return cria_pedra_branca()
    else:
        return cria_pedra_neutra()

def obtem_cadeia(goban, inter):
    """
    Devolve a cadeia de interseções da mesma pedra diretamente conectadas à
    interseção recebida, no goban recebido.
    """
    maxInter = obtem_ultima_intersecao(goban)
    pedra = obtem_pedra(goban, inter)
    cadeia, naoVerificadas = (), [inter]
    
    while naoVerificadas:
        inter = naoVerificadas.pop()
        cadeia += (inter,)
        for adj in obtem_intersecoes_adjacentes(inter, maxInter):
            if obtem_pedra(goban, adj) == pedra and adj not in list(cadeia) + naoVerificadas:
                naoVerificadas.append(adj)             
    return ordena_intersecoes(cadeia)

def coloca_pedra(goban, inter, pedra):
    """
    Modifica o goban passado como argumento, colocando a pedra na interseção
    e devolve o próprio goban.
    """
    str_inter = intersecao_para_str(inter)
    if eh_pedra_branca(pedra):
        goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = "1"
    elif eh_pedra_preta(pedra):
        goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = "2"
    else:
        goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = "0"

    return goban

def remove_pedra(goban, inter):
    """
    Modifica o goban passado como argumento, removendo da interseção a pedra que
    lá esteja.
    """
    str_inter = intersecao_para_str(inter)
    goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = "0"
    return goban

def remove_cadeia(goban, inters):
    """
    Modifica o goban passado como argumento, removendo todas das interseções as 
    pedra que lá estejam.
    """    
    for inter in inters:
        str_inter = intersecao_para_str(inter)
        goban[columnToNum(str_inter[0]) - 1][int(str_inter[1:]) - 1] = "0"

    return goban

def eh_goban(goban):
    """
    Recebe um argumento de qualquer tipo e devolve True se o seu argumento 
    corresponde a um goban e False caso contrário, sem nunca gerar erros
    """
    # chech main goban and first column
    if type(goban) != list :
        return False
    
    length = len(goban)
    if (length != 9 and length != 13 and length != 19) or type(goban[0]) != list:
        return False

    # save height to compare
    height = len(goban[0])
    for index in range(len(goban)):
        
        #check has correct height
        if type(goban[index]) is not list:
            return False
        
        #check length and type of column
        currentLen = len(goban[index])
        if height != currentLen or length != currentLen or type(goban[index]) != list:
            return False
        
        #check elements are P, B or .
        for element in goban[index]:
            if element != "0" and element!= "2" and element != "1":
                return False       

    return True

def eh_intersecao_valida(goban, inter):
    """
    Devolve True a interseção for válida dentro do
    goban g e False caso contrário.
    """
    maxInter = obtem_ultima_intersecao(goban)

    if not eh_intersecao(inter) or not eh_goban(goban):
        return False
    
    strMax = intersecao_para_str(maxInter)
    maxLin = int(strMax[1:])

    str_inter = intersecao_para_str(inter)
    col = columnToNum(str_inter[0])
    lin = int(str_inter[1:])

    # como max coluna = max linha
    if 1 <= col <= maxLin and 1 <= lin <= maxLin and inter == cria_intersecao(obtem_col(inter), obtem_lin(inter)):
        return True
    return False

def gobans_iguais(goban1, goban2):
    """
    Devolve true caso dois gobans sejam iguais e false caso contrário.
    """
    if eh_goban(goban1) and eh_goban(goban2):
        return goban1 == goban2
    return False

def goban_para_str(goban):
    """
    Recebe um goban e devolve a cadeia de caracteres que o representa (a 
    representação externa ou representação “para os nossos olhos”), de acordo 
    com o exemplo na seguinte interação. Se o argumento dado for inválido, a 
    função gera um erro com a mensagem 'territorio_para_str: argumento invalido'.
    """

    def getLetters(width):
        """
        Recebe uma largura e retorna as letras correspondentes, com os respetivos espaçamentos
        para identificar colunas.
        """
        columnNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        letters = "   "
        for letter in range(width):
            letters += columnNames[letter]
            # add spacing
            if not(width-1 == letter):
                letters += " "
        return letters

    height = len(goban[0]) 
    width = len(goban) 
    resultString = ""

    # letras inicias
    resultString += getLetters(width)
    resultString += "\n"

    for rowIndex in range(height-1, -1,-1):
        if rowIndex < 9:
            resultString += " "

        # digitos
        resultString += str(rowIndex + 1) + " "

        # goban
        for colummIndex in range(width):

            if goban[colummIndex][rowIndex] == "2":
                resultString += "X "
            elif goban[colummIndex][rowIndex] == "1":
                resultString += "O "
            else:
                resultString += ". "

        # digitos finais
        if rowIndex < 9:
            resultString += " "
        resultString += str(rowIndex + 1) 
        resultString += "\n"
    
    # letras finais
    resultString += getLetters(width)

    return resultString


##################################################
# Operações de alto nível para goban             #
##################################################

def ordenaCadeias(territorios):
    """
    Devolve as cadeias de interseções ordenadas pelo primeiro elemento de cada uma.
    """
    
    def custom_key(terrs):
        str_inter = intersecao_para_str(terrs[0])
        col = columnToNum(str_inter[0])
        lin = int(str_inter[1:])
        return (lin, col)

    return tuple(sorted(territorios, key=custom_key))

def obtem_territorios(goban):
    """
    Devolve o tuplo de cadeias ordenadas de intersecoes com os tuplos das 
    interseções ordenadas com pedras neutras no goban.
    """

    territorios = ()
    vazios = ()

    strMax = intersecao_para_str(obtem_ultima_intersecao(goban))
    maxCol = int(strMax[1:])

    for col in range(maxCol):
        for lin in range(maxCol):

            interStr = chr(65 + col) + str(lin + 1)
            inter = str_para_intersecao(interStr)

            # se for pedra neutra, obtem cadeia
            # conta vazios para poupar memoria e evitar recursao desnecessária
            if cria_pedra_neutra() == obtem_pedra(goban, inter) and inter not in vazios:
                cadeia = obtem_cadeia(goban, inter)
                if cadeia not in territorios:
                    vazios += cadeia
                    territorios += (cadeia,)
    return ordenaCadeias(tuple(territorios))

def obtem_adjacentes_diferentes(goban, inters):
    """
    Devolve as interseções adjacentes livres, se as interseções do tuplo 
    estão ocupadas por pedras de jogador ou pedras de jogador, se as interseções 
    do tuplo estão livres.
    """
    resultado = ()
    intersType = False

    # se a inicial for de jogador - true
    # se nao - false
    if inters == ():
        return ()
    if obtem_pedra(goban, inters[0]) == cria_pedra_preta() or obtem_pedra(goban, inters[0]) == cria_pedra_branca():
        intersType = True

    for inter in inters:
        for adj in obtem_intersecoes_adjacentes(inter, obtem_ultima_intersecao(goban)):
            if adj not in resultado:
                if not intersType and (obtem_pedra(goban, adj) == cria_pedra_preta() or obtem_pedra(goban, adj) == cria_pedra_branca()):
                    resultado += (adj,)
                if intersType and (obtem_pedra(goban, adj) == cria_pedra_neutra()):
                    resultado += (adj,)
    return ordena_intersecoes(resultado)

def jogada(goban, inter, pedra):
    """
    Modifica o goban colocando a pedra de jogador na interseção e
    remove todas as pedras do jogador contrário pertencentes a cadeias 
    adjacentes à interseção sem liberdades, devolvendo o próprio goban.
    """
    coloca_pedra(goban, inter, pedra)
    cadeiaNaIntersecao = obtem_cadeia(goban, inter)

    # remover jogador contrário
    for adj in obtem_intersecoes_adjacentes(inter, obtem_ultima_intersecao(goban)):
        cadeia = obtem_cadeia(goban, adj)
        if len(obtem_adjacentes_diferentes(goban, cadeia)) == 0 and obtem_pedra(goban, adj) != pedra and cadeia != cadeiaNaIntersecao:
            remove_cadeia(goban, cadeia)
        
    #ve o nossa cadeia
    if len(obtem_adjacentes_diferentes(goban, cadeiaNaIntersecao)) == 0:
       remove_cadeia(goban, cadeiaNaIntersecao)

    return goban

def obtem_pedras_jogadores(goban):
    """
    Devolve um tuplo de dois inteiros que correspondem ao número de 
    interseções ocupadas por pedras do jogador branco e preto, respetivamente.
    """
    numeroBrancas = 0
    numeroPretas = 0

    strMax = intersecao_para_str(obtem_ultima_intersecao(goban))
    maxCol =  int(strMax[1:])

    for col in range(maxCol):
        for lin in range(maxCol):

            interStr = chr(65 + col) + str(lin + 1)
            inter = str_para_intersecao(interStr)

            # se for pedra neutra, obtem cadeia
            # conta vazios para poupar memoria e evitar recursao desnecessária
            pedraAtual = obtem_pedra(goban, inter)
            if cria_pedra_branca() == pedraAtual:
                numeroBrancas += 1
            elif cria_pedra_preta() == pedraAtual:
                numeroPretas += 1
    
    return (numeroBrancas, numeroPretas)


##################################################
# Funções adicionais                             #
##################################################

def calcula_pontos(goban):
    """
    Devolve o tuplo com os pontos de cada jogador, branco e preto, respetivamente.
    """
    # brancas, pretas
    resultado = [0,0]

    strMax = intersecao_para_str(obtem_ultima_intersecao(goban))
    maxLin = int(strMax[1:])

    if goban == cria_goban_vazio(maxLin):
        return (0,0)

    for territorio in obtem_territorios(goban):
        adjs = obtem_adjacentes_diferentes(goban, territorio)

        jogador = obtem_pedra(goban, adjs[0])
        pontos = 0
        terrMau = False
        for adj in adjs:
            if jogador != obtem_pedra(goban, adj):
                terrMau = True
        
        # se o terrorio pertencer a um jogador
        if not terrMau:
            for inter in territorio:
                pontos += 1

        if jogador == cria_pedra_branca():
            resultado[0] += pontos
        elif jogador == cria_pedra_preta():
            resultado[1] += pontos

    numeroPedrasPorJogador = obtem_pedras_jogadores(goban)
    resultado[0] += numeroPedrasPorJogador[0]
    resultado[1] += numeroPedrasPorJogador[1]

    return (resultado[0], resultado[1])


def eh_jogada_legal(goban, inter, pedra, gobanAnterior):
    """
    Devolve true se uma jogada for válida e false caso contrário sem gerar exceções.
    """
    cloneGoban2 = cria_copia_goban(goban)
    
    if not eh_intersecao_valida(goban, inter) or obtem_pedra(goban, inter) != cria_pedra_neutra():
        return False

    jogada(cloneGoban2, inter, pedra)
    for adj in obtem_intersecoes_adjacentes(inter, obtem_ultima_intersecao(goban)):
        cadeia = obtem_cadeia(cloneGoban2, adj)

        # se adj no novo goban for neutro e adj no antigo for a nossa pedra entao desapareceu
        if obtem_pedra(cloneGoban2, adj) == cria_pedra_neutra() and obtem_pedra(goban, adj) == pedra:
            return False
        if len(obtem_adjacentes_diferentes(cloneGoban2, cadeia)) == 0:
            return False
        
    if gobanAnterior == cloneGoban2:
        return False
    
    return True

def turno_jogador(goban, pedra, goban2):
    """
    Recebe um goban, uma pedra de jogador e um outro goban, e permite 
    ao jogador a jogar a opção de passar ou de colocar uma pedra própria 
    numa interseção. Se o jogador passar, a função devolve False sem 
    modificar os argumentos. Caso contrário, a função devolve True e 
    modifica o goban de acordo com a jogada realizada.
    """
    texto = "Escreva uma intersecao ou 'P' para passar [" + pedra_para_str(pedra) + "]:"
    textoIn = input(texto)
    while textoIn != "P":
        try:
            inter = str_para_intersecao(textoIn)
            if eh_jogada_legal(goban, inter, pedra, goban2):
                jogada(goban, inter, pedra)
                return True
        except (ValueError, IndexError):
            pass
        textoIn = input(texto)

    return False

def go(n, brancas, pretas):
    """
    Função principal que permite jogar um jogo completo do Go de dois jogadores. 
    A função recebe um inteiro correspondente à dimensão do tabuleiro, e dois 
    tuplos (potencialmente vazios) com a representação externa das 
    interseções ocupadas por pedras brancas (tb) e pretas (tp) inicialmente. 
    O jogo termina quando os dois jogadores passam a vez de jogar 
    consecutivamente. A funçãao devolve True se o jogador com pedras brancas 
    conseguir ganhar o jogo, ou False caso contrário.
    """
    if (n != 9 and n != 13 and n != 19) :
        raise ValueError("go: argumentos invalidos")

    def obtemIntersecoes(strg, n):
        """
        Devolve as interseções partindo do seu formato externo, validando-as.
        """
        gobanVazio = cria_goban_vazio(n)
        resultado = ()

        if type(strg) != tuple:
            raise ValueError("go: argumentos invalidos")
        for interStr in strg:
            try:
                inter = str_para_intersecao(interStr)
            except (ValueError, IndexError, TypeError):
                raise ValueError("go: argumentos invalidos")
            if not eh_intersecao_valida(gobanVazio, inter):
                raise ValueError("go: argumentos invalidos")
            resultado += (inter,)
        return resultado  
     
    intPretas = obtemIntersecoes(pretas, n)
    intBrancas = obtemIntersecoes(brancas, n)

    try:
        goban = cria_goban(n, intBrancas, intPretas)
    except ValueError:
        raise ValueError("go: argumentos invalidos")

    # print inicial
    pontos = calcula_pontos(goban)
    print(f'Branco (O) tem {pontos[0]} pontos\nPreto (X) tem {pontos[1]} pontos')
    print(goban_para_str(goban))

    jogoDecorrer = [True]
    jogadorAnteriorPassou = [False]

    # joga e ve se ja houve 2 passes consecutivos
    def turno(pedra, passou, aCorrer , gobanMesmoJogadorAnterior):
        """
        Modificando o goban aplicando-lhe um turno. Averigua se ambos os jogadores
        passaram. Imprime na consola os pontos e o goban.
        """
        if not turno_jogador(goban, pedra, cria_copia_goban(gobanMesmoJogadorAnterior)): # novo goban
            if passou[0]:
                aCorrer[0] = False
            else:
                passou[0] = True
        else:
            passou[0] = False

        pontos = calcula_pontos(goban)
        print(f'Branco (O) tem {pontos[0]} pontos\nPreto (X) tem {pontos[1]} pontos')
        print(goban_para_str(goban))
        return goban
    
    # guarda gobans anteriores para evitar voltar ao mesmo estado
    gobanPretoAnterior = gobanBrancoAnterior = cria_goban_vazio(n)

    # enquanto o jogo decorrer
    while jogoDecorrer[0]:
        
        gobanPretoAnterior = turno(cria_pedra_preta(), jogadorAnteriorPassou, jogoDecorrer, gobanPretoAnterior)
        if jogoDecorrer[0]:
            gobanBrancoAnterior = turno(cria_pedra_branca(), jogadorAnteriorPassou, jogoDecorrer, gobanBrancoAnterior)

    pontos = calcula_pontos(goban)
    if pontos[0] >= pontos[1]:
        return True
    return False  
