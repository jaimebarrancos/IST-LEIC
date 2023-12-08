# Jaime Ribeiro Barrancos


def eh_territorio(territory):
    """
    Recebe um argumento de qualquer tipo e devolve True se o seu argumento 
    corresponde a um território e False caso contrário, sem nunca gerar erros
    """

    # chech main territory and first column
    if type(territory) != tuple or territory == () or type(territory[0]) != tuple:
        return False

    length = len(territory)
    if not(1 <= length < 27):
        return False
    
    # save height to compare
    height = len(territory[0])
    for index in range(len(territory)):
        
        #check has correct height
        if type(territory[index]) is not tuple:
            return False
        
        #check length and type of column
        currentLen = len(territory[index])
        if height != currentLen or not(1 <= currentLen < 100) or type(territory[index]) != tuple:
            return False
        
        #check elements are 1 or 0 (have to be ints)
        for element in territory[index]:
            if type(element) != int or (element != 0 and element!= 1):
                return False       

    return True

######################################################


def obtem_ultima_intersecao(territory):
    """
    Recebe um território e devolve a intersecao do extremo superior 
    direito do território.
    """

    columnNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # get total height and length
    height = len(territory[0])
    length = len(territory)    

    return (columnNames[length-1], height)

######################################################


def eh_intersecao(intersection):
    """
    Recebe um argumento de qualquer tipo e devolve True se o seu 
    argumento corresponde a uma interseção e False caso contrário, 
    sem nunca gerar erros.
    """

    columnNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # check is tuple with 2 elements
    if type(intersection) != tuple or len(intersection) != 2:
        return False
    # check elements are appropriate
    if type(intersection[1]) == int and type(intersection[0]) == str and  1 <= intersection[1] < 100:
        # check is a single letter that is in columnNames
        for letter in columnNames:
            if letter == intersection[0]:
                return True
    return False

######################################################


def eh_intersecao_valida(territory, intersection):
    """
    Recebe um território e uma interseção, e devolve True se a
    interseção corresponde a uma interseção do território, e False caso contrário.
    """

    # is empty tuple
    if intersection == ():
        return False
    
    #is first element str and second int
    if type(intersection[0]) != str or type(intersection[1]) != int:
        return False
    
    height = len(territory[0])
    length = len(territory)

    letterOrd = columnToNum(intersection[0])

    #check is between length and height limits
    if 65 <= letterOrd + 65 <= 65 -1 + length and 1 <= intersection[1] <= height:
        return True
    return False

######################################################


def eh_intersecao_livre(territory, intersection):
    """
    Recebe um território e uma interseção do território, e devolve True
    se a interseção corresponde a uma interseção livre (não ocupada por montanhas) 
    dentro do território e False caso contrário.
    """

    verticalLocation = intersection[1] - 1 # because index starts at 0

    # get index corresponding to the letter
    horizontalLocation = columnToNum(intersection[0])

    if territory[horizontalLocation][verticalLocation] == 0:
        return True
    return False

######################################################


def obtem_intersecoes_adjacentes(territory, intersection):
    """
    Recebe um território e uma interseção do território, e devolve o tuplo 
    formado pelas interseção válidas adjacentes da interseção em ordem de 
    leitura de um território.
    """

    # get index corresponding to the letter
    verticalLocation = intersection[1] # because index starts at 0
    horizontalLocation = 0

    #get index of corresponding letter

    horizontalLocation = columnToNum(intersection[0])

    #get each intersection ord(A) = 65, ord(Z) = 25 + 65
    downIntersection = (chr(horizontalLocation + 65), verticalLocation - 1)
    leftIntersection = (chr(horizontalLocation + 65 - 1), verticalLocation)
    if horizontalLocation != 26 - 1:
        rightIntersection = (chr(horizontalLocation + 65 + 1), verticalLocation)
    else:
        rightIntersection = ()

    upIntersection = (chr(horizontalLocation + 65), verticalLocation + 1)

    resultIntersections = ()
    #check if each one is valid to add to result
    for intersection in (downIntersection, leftIntersection, rightIntersection, upIntersection):
        if eh_intersecao_valida(territory, intersection):
            resultIntersections += (intersection,)

    return resultIntersections

######################################################


def ordena_intersecoes(intersections):
    """
    Função recursiva que recebe um tuplo de interseções (potencialmente vazio) e devolve um tuplo 
    contendo as mesmas interseções ordenadas de acordo com a ordem de 
    leitura do território.
    """

    resultIntersections = ()
    
    if intersections == ():
        return ()

    for index in range(len(intersections) - 1):

        if index == 0:
            startElements = ()
        else:
            startElements = intersections[:index]
        
        # order numbers first 
        if intersections[index + 1][1] < intersections[index][1]:
            # switch and call the function with the switched elements tuple
            resultIntersections = startElements + (intersections[index + 1],) + (intersections[index],) + intersections[index + 2:]
            return ordena_intersecoes(resultIntersections)
        
        # order letters only if not undoing the order numbers
        if (intersections[index + 1][1] == intersections[index][1]) and intersections[index + 1][0] < intersections[index][0]:
            # switch and call the function with the switched elements tuple
            resultIntersections = startElements + (intersections[index + 1],) + (intersections[index],) + intersections[index + 2:]
            return ordena_intersecoes(resultIntersections)

    return intersections

######################################################


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

######################################################


def territorio_para_str(territory):
    """
    Recebe um território e devolve a cadeia de caracteres que o representa (a 
    representação externa ou representação “para os nossos olhos”), de acordo 
    com o exemplo na seguinte interação. Se o argumento dado for inválido, a 
    função gera um erro com a mensagem 'territorio_para_str: argumento invalido'.
    """

    if not eh_territorio(territory):
        raise ValueError("territorio_para_str: argumento invalido")

    height = len(territory[0]) 
    width = len(territory) 
    resultString = ""

    # start letters
    resultString += getLetters(width)
    resultString += "\n"

    for rowIndex in range(height-1, -1,-1):
        if rowIndex < 9:
            resultString += " "

        # start digit
        resultString += str(rowIndex + 1) + " "

        # territory
        for colummIndex in range(width):

            if territory[colummIndex][rowIndex] == 0:
                resultString += ". "
            else:
                resultString += "X "

        # end digit and new line
        if rowIndex < 9:
            resultString += " "
        resultString += str(rowIndex + 1) 
        resultString += "\n"
    
    # end letters
    resultString += getLetters(width)

    return resultString

######################################################
######################################################
######################################################


def columnToNum(letter): # starts at 0
    """
    Recebe uma letra e devolve o index correspondente a essa letra no abcedário.
    """

    # number corresponding to letter
    letterOrd = ord(letter)

    # index of that number in a territory
    return letterOrd - 65

###################################################### 


def getConnectedIntersections(territory, intersectionsToConnect, intersectionOriginalNum, pos):
    """
    Função recursiva que recebe um território e um tuplo com interseções e 
    retorna as interseções do mesmo tipo diretamente conectadas a cada interseção
    no tuplo de interseções. 
    """

    intersectionNum = territory[columnToNum(pos[0])][pos[1] - 1] # 1 or 0
    if (pos not in intersectionsToConnect and intersectionNum == intersectionOriginalNum):
        # add current intersection
        intersectionsToConnect += (pos,)

    # for each adjacent intersection
    for adj in obtem_intersecoes_adjacentes(territory, pos):
        # mountain = 1, free = 0
        intersectionNum = territory[columnToNum(adj[0])][adj[1] - 1] # 1 or 0
        if (intersectionNum == intersectionOriginalNum and adj not in intersectionsToConnect):
            # for each intersection connected to pos
            for connectedIntersection in getConnectedIntersections(territory, intersectionsToConnect, intersectionOriginalNum, adj):
                if connectedIntersection not in intersectionsToConnect:
                    intersectionsToConnect += (connectedIntersection,)

    return intersectionsToConnect

######################################################


def obtem_cadeia(territory, intersection):
    """
    Recebe um território e uma interseção do território (ocupada por 
    uma montanha ou livre), e devolve o tuplo formado por todas as 
    interseção que estão conectadas a essa interseção ordenadas 
    (incluida si própria) de acordo com a ordem de leitura de um território. 
    Se algum dos argumentos dado for inválido, a função deve gerar um erro 
    com a mensagem 'obtem_cadeia: argumentos invalidos'.
    """

    if not eh_territorio(territory) or not eh_intersecao_valida(territory, intersection):
        raise ValueError("obtem_cadeia: argumentos invalidos")
    
    # order the final result
    return ordena_intersecoes(getConnectedIntersectionsOfSameType(territory, intersection))

######################################################


def getConnectedIntersectionsOfSameType(territory, intersection):
    """
    Recebe um território e uma interseção do território (ocupada por 
    uma montanha ou livre), e devolve o tuplo formado por todas as 
    interseção que estão conectadas a essa interseção ordenadas 
    (incluida si própria) de acordo com a ordem de leitura de um território. 
    """
    columnIndex = columnToNum(intersection[0])

    # True - free,  False - mountain
    intersectionType = territory[columnIndex][intersection[1]-1]
    
    return getConnectedIntersections(territory, (), intersectionType, intersection)


######################################################


def obtem_vale(territory, intersection):
    """
    Recebe um território e uma interseção do território ocupada por 
    uma montanha, e devolve o tuplo (potencialmente vazio) formado por 
    todas as interseções que formam parte do vale da montanha da interseção
    fornecida como argumento ordenadas de acordo à ordem de leitura de um 
    território. Se algum dos argumentos dado for inválido, a função deve 
    gerar um erro com a mensagem 'obtem_vale: argumentos invalidos'.
    """

    if not eh_intersecao_valida(territory, intersection) or not eh_territorio(territory) or eh_intersecao_livre(territory, intersection):
        raise ValueError("obtem_vale: argumentos invalidos")

    result = ()
    
    for mountain in obtem_cadeia(territory, intersection):
        for adjacentIntersection in obtem_intersecoes_adjacentes(territory, mountain):
            if eh_intersecao_livre(territory, adjacentIntersection) and adjacentIntersection not in result:
                result += (adjacentIntersection,)
    return ordena_intersecoes(result)

######################################################
######################################################
######################################################


def verifica_conexao(territory, intersection1, intersection2):
    """
    Recebe um território e duas interseções do território e devolve True se 
    as duas interseções estão conetadas e False caso contrário. Se algum 
    dos argumentos dado for inválido, a função deve gerar um erro com a 
    mensagem 'verifica_conexao: argumentos invalidos'.
    """

    if not eh_territorio(territory) or not eh_intersecao_valida(territory, intersection1) or not eh_intersecao_valida(territory, intersection2):
        raise ValueError("verifica_conexao: argumentos invalidos")
    
    intersectionType = territory[columnToNum(intersection1[0])][intersection1[1] - 1]

    # if intersection is in the connected intersections of any type (True or False = mountain or free)
    if intersection2 in getConnectedIntersections(territory, (), intersectionType, intersection1):
        return True
    return False

######################################################


def calcula_numero_montanhas(territory):
    """
    Recebe um território e devolve o número de interseções ocupadas por 
    montanhas no território. Se o argumento dado for inválido, a função 
    deve gerar um erro com a mensagem 'calcula_numero_montanhas: argumento invalido'.
    """

    mountainCount = 0
    if eh_territorio(territory):
        # for each intersection
        for column in territory:
            for element in column:
                # if it's a mountain add 1
                if element == 1:
                    mountainCount += 1
        return mountainCount
    
    raise ValueError("calcula_numero_montanhas: argumento invalido")

######################################################


def calcula_numero_cadeias_montanhas(territory):
    """
    Recebe um território e devolve o número de cadeias de montanhas contidas no 
    território. Se o argumento dado for inválido, a função deve gerar um erro com a 
    mensagem 'calcula_numero_cadeias_montanhas: argumento invalido'.
    """

    mountainChainCount = 0
    totalChain = ()

    if eh_territorio(territory):
        # for each intersection
        for columnIndex in range(len(territory)):
            for index in range(len(territory[columnIndex])):
                
                # if its a mountain
                if territory[columnIndex][index] == 1:
                    # get hole mountain chain connected to this intersection
                    mountainChain = ordena_intersecoes(getConnectedIntersectionsOfSameType(territory, (chr(columnIndex + 65), index + 1))) # faster way to get intersection
                    if mountainChain not in totalChain:
                        totalChain += (mountainChain,)
                        mountainChainCount += 1

        return mountainChainCount
    
    raise ValueError("calcula_numero_cadeias_montanhas: argumento invalido")

######################################################


def calcula_tamanho_vales(territory):
    """
    Recebe um território e devolve o número total de interseções diferentes que 
    formam todos os vales do território. Se o argumento dado for inválido, 
    a função deve gerar um erro com a mensagem 'calcula_tamanho_vales: 
    argumento invalido'.
    """

    if not eh_territorio(territory):
        raise ValueError("calcula_tamanho_vales: argumento invalido")

    totalMountainChainIntersections = ()
    valeIntersections = ()
    sum = 0

    # for each element in the territory
    for columnIndex in range(len(territory)):
        for index in range(len(territory[columnIndex])):

            intersection = (chr(columnIndex + 65), index + 1)

            # if the intersection is valid and free
            if eh_intersecao_valida(territory, intersection) and not eh_intersecao_livre(territory, intersection):
                
                # add intersection to total intersections (mountain intersections)
                if intersection not in totalMountainChainIntersections:
                    currentChain = obtem_cadeia(territory, intersection)
                    for intersec in currentChain:
                        totalMountainChainIntersections += (intersec,)

                # if adjacent is not a mountain then it's a vale adjacent to a mountain
                for adjacent in obtem_intersecoes_adjacentes(territory, intersection):
                    if adjacent not in valeIntersections and eh_intersecao_livre(territory, adjacent):
                        valeIntersections += (adjacent,)
                        sum +=1
    return sum