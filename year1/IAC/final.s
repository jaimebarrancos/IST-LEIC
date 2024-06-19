#
# IAC 2023/2024 k-means
# 
# Grupo: 32
# Campus: Alameda
#
# Autores:
# 109262, Jaime Barrancos
# 109955, Diogo Carreira
# 110754, Rita Líbano Monteiro
#
# Tecnico/ULisboa

# Variaveis em memoria
.data

#Input A - linha inclinada
#n_points: .word 61
#points: .word 1,1, 2,2, 3,3, 4,4, 5,5, 6,6, 7,7, 8,8, 9,9, 10,10, 11,11, 12,12, 13,13, 14,14, 15,15, 16,16, 17,17, 18,18, 19,19, 20,20, 21,21, 22,22, 23,23, 24,24, 25,25, 26,26, 27,27, 28,28, 29,29, 30,30, 31,31, 32,32, 31,30, 30,29, 29,28, 28,27, 27,26, 26,25, 25,24, 24,23, 23,22, 22,21, 21,20, 20,19, 19,18, 18,17, 17,16, 16,15, 15,14, 14,13, 13,12, 12,11, 11,10, 10,9, 9,8, 8,7, 7,6, 6,5, 5,4, 4,3, 3,2, 2,1        

#Input B - Cruz
#n_points:    .word 5
#points:     .word 4,2, 5,1, 5,2, 5,3 6,2

#Input C
#n_points:    .word 23
#points: .word 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 1,3, 2,0, 2,1, 5,3, 6,2, 6,3, 6,4, 7,2, 7,3, 6,8, 6,9, 7,8, 8,7, 8,8, 8,9, 9,7, 9,8

#Input D
n_points:    .word 30
points:      .word 16, 1, 17, 2, 18, 6, 20, 3, 21, 1, 17, 4, 21, 7, 16, 4, 21, 6, 19, 6, 4, 24, 6, 24, 8, 23, 6, 26, 6, 26, 6, 23, 8, 25, 7, 26, 7, 20, 4, 21, 4, 10, 2, 10, 3, 11, 2, 12, 4, 13, 4, 9, 4, 9, 3, 8, 0, 10, 4, 10

#Input Ew
#n_points:    .word 5
#points:      .word 16, 1, 17, 31, 18, 6, 20, 3, 21, 20
# Valores de centroids e k a usar na 1a parte do projeto:
#centroids:   .word 0,0
#k:           .word 2

# Valores de centroids, k e L a usar na 2a parte do projeto:
centroids:   .word 0,0, 0,0, 0,0
k:           .word 3
L:           .word 10

# Associates a cluster to it's respective point. The index of the point in the
# points vector is the same as it's index in the clusters vector
clusters:    .zero 120 # number of points * 4

# Stores auxiliary data. Has 3 numbers per cluster: accumulative sum of x and y 
# and the number of points in that cluster
aux_sum:     .zero 36 # number of clusters * 4 * 3

colors:      .word 0xff0000, 0x00ff00, 0x0000ff,0x1230ff  # Colors of each cluster 0, 1, 2, etc.

.equ         black      0
.equ         white      0xffffff


# Codigo
.text
    jal mainKMeans
    
    li a7, 10
    ecall


### printPoint
# Pinta o ponto (x,y) na LED matrix com a cor passada por argumento
# Nota: a implementacao desta funcao ja' e' fornecida pelos docentes
# E uma funcao auxiliar que deve ser chamada pelas funcoes seguintes que pintam a LED matrix.
# Argumentos:
# a0: x
# a1: y
# a2: cor

printPoint:
    li a3, LED_MATRIX_0_HEIGHT
    sub a1, a3, a1
    addi a1, a1, -1
    li a3, LED_MATRIX_0_WIDTH 
    mul a3, a3, a1
    add a3, a3, a0
    slli a3, a3, 2
    li a0, LED_MATRIX_0_BASE
    add a3, a3, a0   # addr
    sw a2, 0(a3)
    jr ra
    

### cleanScreen
# Limpa todos os pontos do ecrã
# Argumentos: nenhum
# Retorno: nenhum
cleanScreen:
    # store ra
    li t0 LED_MATRIX_0_WIDTH # max width
    li t1 LED_MATRIX_0_HEIGHT # max height
    li t3 LED_MATRIX_0_BASE # base address
    mul t2 t0 t1 # size of stack
    slli t2 t2 2

    li t4 0 # current i
    li t6 white
    
    #OPTIMIZATION
    # Traverse memory directly with only
    # one loop instead and change color manually
    # (instead of calling print point)
    
    for_clean:
    bge t4 t2  end_clean
    add t5, t3, t4 # t5 is current address
    
    #OPTIMIZATION
    # color 4 points at a time to
    # make use of fewer instructions
    sw t6, 0(t5) # place colors
    sw t6, 4(t5)
    sw t6, 8(t5)
    sw t6, 12(t5) 
    
    addi t4 t4 16
    j for_clean
    end_clean:    
    
    jr ra
    
    
### printClusters
# Pinta os agrupamentos na LED matrix com a cor correspondente.
# Argumentos: nenhum
# Retorno: nenhum

printClusters:
    la t0 points
    li t1 0 # current i
    lw t2 n_points
    slli t2 t2 3

    la t3 colors
    la t4 clusters

    for_point: # break if counter >= number points
    bge t1 t2 end_point
    
    # get index of cluster
    srai t5 t1 1
    add t5 t5 t4
    
    # get color of cluster
    lw t6 0(t5) # get which cluster the point belongs to
    slli t6 t6 2
    add t5 t3 t6 # get color address
    lw a2 0(t5) # set colour
    
    # t5 is now for a different use: the current point address
    add t5 t0 t1 
    
    lw a0 0(t5)
    lw a1 4(t5)
    addi sp sp -4
    sw ra 0(sp)
    jal printPoint
    lw ra 0(sp)
    addi sp sp 4
    
    addi t1 t1 8 # increment counter
    j for_point
    
    end_point:    
    jr ra  


### printCentroids
# Pinta os centroides na LED matrix
# Nota: deve ser usada a cor preta (black) para todos os centroides
# Argumentos: nenhum
# Retorno: nenhum

printCentroids:
    la t0 centroids
    li a2 black
    lw t3 k

    for_centroid:
    beqz t3 end_for_centroid
    
    lw a0 0(t0)
    lw a1 4(t0)

    # setup and call print point
    addi sp sp -4
    sw ra 0(sp)
    jal printPoint
    lw ra 0(sp)
    addi sp sp 4
    
    # update counters
    addi t3 t3 -1
    addi t0 t0 8
    j for_centroid
    
    end_for_centroid:
    jr ra


### calculateCentroids
# Calcula os k centroides, a partir da distribuicao atual de pontos associados a cada agrupamento (cluster)
# Argumentos: nenhum
# Retorno: 
# a0: Number of equal centroids

#OPTIMIZATION: return the number of equal centroids
# instead of copying all of them and checking if they
# are the same.

calculateCentroids:
    # store saved registers
    addi sp sp -48
    sw s0 0(sp) # index points
    sw s1 4(sp) # cluster index
    sw s2 8(sp) # n points
    sw s3 12(sp) # points
    sw s4 16(sp) # clusters
    sw s5 20(sp) # aux_sum
    sw s6 24(sp) # x
    sw s7 28(sp) # y
    sw s8 32(sp) # count
    sw s9 36(sp) # x count
    sw s10 40(sp) # y count
    sw s11 44(sp) # check for equal
    
    li s0 0
    li t0 0 #prev x
    li t1 0 #prev y
    li s11 0

    lw s2 n_points
    la s3 points
    la s4 clusters
    la s5 aux_sum
    li t0 12
    
    # accumulate x and y of each cluster based on 
    # the cluster each point belongs to
    
    while_cc:
        beq s0 s2 end_while_cc
        lw s6 0(s3) # x
        lw s7 4(s3) # y
        lw s1 0(s4) # cluster index
        mul s1 s1 t0
        add s1 s1 s5
        lw s9 0(s1) # x count
        lw s10 4(s1) # y count
        lw s8 8(s1) # count
        add s9 s9 s6
        add s10 s10 s7
        addi s8 s8 1
        sw s9 0(s1)
        sw s10 4(s1)
        sw s8 8(s1)
        addi s3 s3 8
        addi s4 s4 4
        addi s0 s0 1
        j while_cc
        
    end_while_cc:
        # calculate average
        lw s0 k 
        la s1 centroids
        while_cc2:
            beqz s0 end_while_cc2
            lw s9 0(s5) # x count
            lw s10 4(s5) # y count
            lw s8 8(s5) # count
            div s9 s9 s8 # centroid x
            div s10 s10 s8 # centroid y
            
            lw t0 0(s1)
            lw t1 4(s1)
            
            # check if all centroids are the same
            sub t0 t0 s9
            sub t1 t1 s10
            
            bge t0, zero, second_neg  
            neg t0, t0          
            second_neg:
            bge t1, zero, positive  
            neg t1, t1  

            positive:
            add t0 t0 t1 # if point is equal to previous 
            # the sum of t0 and t1 must be 0, if t0 
            # is different from zero then dont add 1
            bnez t0 continue
            addi s11 s11 1 
            
            continue:
                sw s9 0(s1)
                sw s10 4(s1)
                addi s5 s5 12
                addi s1 s1 8
                addi s0 s0 -1
                j while_cc2
        
        end_while_cc2:
            mv a0 s11 # return value
            # load saved registers
            lw s0 0(sp)
            lw s1 4(sp)
            lw s2 8(sp)
            lw s3 12(sp)
            lw s4 16(sp)
            lw s5 20(sp)
            lw s6 24(sp)
            lw s7 28(sp)
            lw s8 32(sp)
            lw s9 36(sp)
            lw s10 40(sp)
            lw s11 40(sp)
            addi sp sp 48
            jr ra
            

### manhattanDistance
# Calcula a distancia de Manhattan entre (x0,y0) e (x1,y1)
# Argumentos:
# a0, a1: x0, y0
# a2, a3: x1, y1
# Retorno:
# a0: distance

manhattanDistance:
    li t0, -1
    sub t1, a0, a2
    sub t2, a1, a3
    
    # check if is positive
    bgez t1, second_point
    mul t1, t1, t0
    
    second_point:
        bgez t2, final
        mul t2, t2, t0
        
    final:
        add a0, t1, t2
        
    jr ra


### nearestCluster
# Determina o centroide mais perto de um dado ponto (x,y).
# Argumentos:
# a0, a1: (x, y) point
# Retorno:
# a0: cluster index

nearestCluster:
    
    # store s
    addi sp sp -24
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    
    lw s0 k
    la s1 centroids
    li s2 0 # current cluster index
    li s3 0 # current nearest cluster
    li s4 64 # current smallest manhattan distance
    
    addi s5 a0 0 # store x of centroid
    
    for_cluster:
        beq s0 s2 end_for_cluster # break after going through all clusters
        
        addi a0 s5 0
        lw a2 0(s1) # load arguments for second point
        lw a3 4(s1)
        addi sp sp -4 # prepare jal
        sw ra 0(sp)
        jal manhattanDistance
        lw ra 0(sp)
        addi sp sp 4
    
        # if return is bigger than t6, dont change t6
        bge a0 s4 dont_change
        addi s4 a0 0
        addi s3 s2 0 

        dont_change:
        addi s1 s1 8 # increment current points
        addi s2 s2 1 # increment cluster index
        j for_cluster
    
    end_for_cluster:
    addi a0 s3 0
    
    # load s
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    addi sp sp 24
    
    jr ra    


### populateClusters
# Coloca o índice de k-1 centroides mais proximo de cada ponto (x,y).
# Argumentos: nenhum
# Retorno: nenhum

#OPTIMIZATION: auxiliary function to run nearest cluster
# for every point (populating the clusters vector)

populateClusters:
# store saved registers
     addi sp sp -20
     sw ra 0(sp)
     sw s0 4(sp)
     sw s1 8(sp)
     sw s2 12(sp)
     sw s3 16(sp)
     li s3 0
     lw s0 n_points
     la s1 points
     la s2 clusters
     
     while_nc:
         beq s3 s0 end_while_nc
         lw a0 0(s1)
         lw a1 4(s1)
         jal nearestCluster
         sw a0 0(s2)
         # increment counters
         addi s3 s3 1
         addi s1 s1 8
         addi s2 s2 4
         j while_nc
         
    end_while_nc:
        # load saved registers
        lw ra 0(sp)
        lw s0 4(sp)
        lw s1 8(sp)
        lw s2 12(sp)
        lw s3 16(sp)
        addi sp sp 20
        jr ra

### indexCentroid
# Gera um número aleatório de 1 até R = n_points/k.
# Argumentos:
# a0: R
# Retorno: 
# a0: Random number [1,R]

indexCentroid:
    # store s
    addi sp sp -20
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    sw s3 16(sp)
    
    ## Perform the mod calculation: c % R
    mv s0 a0 # R
    li a7 30
    ecall
    
    # if is negative switch to positive
    bge a0, x0, is_positive
    neg a0, a0          
    is_positive:

    mv s1 a0 # c
    
    div s2 s1 s0          # s2 = c%R
    mul s3 s2 s0          # S2 * R
    sub a0 s1 s3          # Resto = R - S2*R
    
   bnez a0 continue_index_centroid
   mv a0 s0
   continue_index_centroid: 
    lw ra 0(sp)
    lw s0 4(sp)
    lw s1 8(sp)
    lw s2 12(sp)
    lw s3 16(sp)
    addi sp sp 20
    jr ra
    



### initializeCentroids
# Inicializa os valores iniciais do vetor centroids.
# Um valor entre 1 e a média do número de pontos é somado ao 
# endereço do vetor points.
# Argumentos: nenhum
# Retorno: nenhum

initializeCentroids:
    # store s
    addi sp sp -20
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    sw s3 16(sp)
    lw s0 n_points
    lw s1 k
    la s2 points
    la s3 centroids
    li t0 0 #x
    li t1 0 #y
    
    div s0 s0 s1
    mv a0 s0
    
    addi sp sp -4
    sw ra 0(sp)
    jal indexCentroid
    lw ra 0(sp)
    addi sp sp 4
    
    mv s0 a0 # Random
    slli s0 s0 3 
    
    while_init_c:
        beqz s1 end_while_init
        lw t0 0(s2) # load the point and store it in centroids
        lw t1 4(s2)
        sw t0 0(s3)
        sw t1 4(s3)
        
        # iter
        addi s1 s1 -1
        addi s3 s3 8 # through centroids 
        add s2 s2 s0 # through points (bigger jump)
        j while_init_c
        
    end_while_init: 
        lw ra 0(sp)
        lw s0 4(sp)
        lw s1 8(sp)
        lw s2 12(sp)
        lw s3 16(sp)
        addi sp sp 20
        jr ra
    
    
### mainKMeans
# Executa o algoritmo *k-means*.
# Argumentos: nenhum
# Retorno: nenhum

mainKMeans:  
    addi sp sp -16
    sw ra 0(sp)
    sw s0 4(sp)
    sw s1 8(sp)
    sw s2 12(sp)
    
    lw s0 L
    lw s1 k
    lw s2 0
    
    jal initializeCentroids
    
    while_kmeans: 
        beqz s0 end_while_kmeans # Do L iteractions 
        beq s1 s2 end_while_kmeans # if the number of equal points is equal to k break
        jal cleanScreen
        jal populateClusters
        jal printClusters
        jal calculateCentroids
        mv s2 a0
        jal printCentroids
        
        #iter
        addi s0 s0 -1
        j while_kmeans
    
    end_while_kmeans:
        lw ra 0(sp)
        lw s0 4(sp)
        lw s1 8(sp)
        lw s2 12(sp)
        addi sp sp 16
        jr ra
