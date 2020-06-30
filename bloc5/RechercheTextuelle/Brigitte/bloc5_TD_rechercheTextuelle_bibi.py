################################################
##  Recherche de motifs exacts                ##
##    Algorithme naïf                         ##
################################################
print('Algo naïf')

T = "GCATCGCAGAGAGTATACAGTACG"
M = "GCAGAGAG"
#M = "CCGGTGAA"
#T = "AAAAAAAAAAAAAAAAAAAA"
#M = "AAAAAA"
#T = "GCATACGCACGCAAGAGAGTATACGCATACG"
#M = "ACGT"
#M = "ACGCA"


#  Première implémentation avec all

def naif(texte, motif) :
    res = []
    for i in range(len(texte)-len(motif)+1):
        ok = all([texte[i+j]==motif[j] for j in range(len(motif))])
        if ok == True :
            res.append(i)
    return res
print(naif(T,M))

#  Deuxième implémentation en comptant le nombre d'opératins effectuées

def rechercheAlgoNaifNbOp(texte, motif) :
    m = len(motif)
    n = len(texte)
    res = []
    comp = 0
    # boucle pour faire glisser le motif sous le texte à partir de zéro an faisant attention de ne pas dépasser ! 
    for i in range(n-m+1) :
        j = 0
        while j <= m-1 and texte[i+j] == motif[j] :
            j += 1
            comp += 1
        if j == m :
            res. append(i)
        else :
            comp += 1 # pour ne pas oublier de compter les échecs de comparaison (mismatch)
    return "Motif trouvé en " + str(comp) + ' comparaisons, en position(s) : ' + str(res)
print(rechercheAlgoNaifNbOp(T,M))


#  Troisième implémentation avec amélioration en ragardant si les lettres du motif sont toutes différentes...

def rechercheAlgoNaif(texte, motif) :
    m = len(motif)
    n = len(texte)
    res = []
    # on teste pour savoir si les lettres du motif sont différentes afin d'accélérer le pgm naif dans ce cas
    lettresDiff = True
    for i in range(m) :
        if motif[i] in motif[i+1:] :
            lettresDiff = False
            break
    print('Lettres du motif différentes : ',lettresDiff)
    # boucle pour faire glisser le motif sous le texte à partir de zéro an faisant attention de ne pas dépasser ! 
    for i in range(n-m) :
        j = 0
        while j <= m-1 and texte[i+j] == motif[j] :
            j += 1
        if j == m :
            res. append(i)
        if lettresDiff == False :
            i += 1
        else :  # on décale directement de j car on sait que motif[j-1] est ok et qu'on ne la retouve pas avt...
            i += max(1,j)    #pour éviter le cas j=0
    return "Motif trouvé en " + str(res)
print(rechercheAlgoNaif(T,M))


################################################
##  Recherche de motifs exacts                ##
##    Heuristique du Mauvais Caractère (MC)   ##
################################################

# Sitographie :    
# * [https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm)
# * [http://whocouldthat.be/visualizing-string-matching/](http://whocouldthat.be/visualizing-string-matching/)

print('MC')

def mauvaisCarac(motif, sigma) :
    """Retourne un dictionnaire avec pour chaque caractère de l'alphabet sigma, le nombre de décalage 
    à partir de la fin du motif avant de trouver ce caractère
    On ne compte pas la dernière lettre du motif et le décalage vaut m = len(motif)"
    si on ne trouve pas le caractère"""
    s = len(sigma)
    m = len(motif)
    MC = {lettre : m for lettre in sigma}   
    for i in range(m-1) :   #ainsi on se s'occupe pas de la lettre en m-1
        #au pire on écrase les valeurs des lettres qui ont plusieurs occurence en gardant la dernière valeur
        MC[motif[i]] = m-i-1   #le -1 c'est parce qu'on commence à zero
    return MC

print(mauvaisCarac('GCAGAGAG', 'ACGT'))
# {'A': 1, 'C': 6, 'G': 2, 'T': 8}

#recherche textuelle avec cette heuristique du Mauvais Caractère

def rechercheMCNbOp(texte, motif) :
    m = len(motif)
    n = len(texte)
    res = []
    comp = 0
    MC = mauvaisCarac(motif, alphabet)
    #boucle pour faire glisser le motif sous le texte à partir de zéro an faisant attention de ne pas dépasser ! 
    i = 0
    while i <= n-m :
        j = m - 1             #on commene à la fin du motif !
        while j >= 0 and texte[i+j] == motif[j] :   #on incrémente tant que c'est identique
            j -= 1
            comp += 1
        if j == -1 :          #motif trouvé!!
            res. append(i)
            i += 1            #il pourrait y avoir une cle style AA..
        else :
            i += max(1, MC[texte[i+j]] - m + 1 + j)   #peut être négatif si le mauvais caractère est dans le suffixe !
            #le décalage correspond au (décalage du MC) - (taille du sous-motif Suffixe M' = m-1 - j)
            comp += 1         #pour ne pas oublier de compter les échecs de comparaison (mismatch)
    return "Motif trouvé en " + str(comp) + ' comparaisons, en position(s) : ' + str(res)

alphabet = ["A", "C", "G", "T"]
print(rechercheMCNbOp(T,M))
# Motif trouvé en 15 comparaisons, en position(s) : [5]


################################################
##  Recherche de motifs exacts                ##
##    Heuristique du Bon Suffixe (BS)         ##
################################################

print('BS')

def plusLongSuffixePrefixe(motif) :
    """ renvoie une liste contenant l'indice du début du plus long suffixe qui est aussi préfixe dans le sous-motif qui
    démarre à j+1. S'il n'y en a pas, on écrit 1. On interdit le mot entier. En particulier SP[m-1]=1"""
    m = len(motif)
    SP = [1]*m
    for j in range(m-1) :      #boucle pour remplir SP de0 à m-2 car SP[m-1]=1
        p = j+1
        while p <= m-1 and motif[p:] != motif[:m-p] :      #boucle sur p croissant car plus p est petit, plus le suffixe est long
            p += 1
        SP[j] = p
    return SP                #pour que l'on retourne 1 dans le pire des cas du bonSuffixe   
print(plusLongSuffixePrefixe('GCAGAGAG'))
#[7, 7, 7, 7, 7, 7, 7, 1]
print(plusLongSuffixePrefixe('ABABA'))
#[2, 2, 4, 4, 1]

def bonSuffixe(motif):
    """ renvoie un tableau où la valeur d'index j est j-k-1 lorsqu'il existe k correspondant 
    à la plus grande position dans le motif où M[j+1..m-1]=[k..m-j-1] et [j]!=M[k-1]
    et lorsqu'il n'existe pas de k on met la valeur correspondante du plusLongSuffixePrefixe(motif) ! """
    m = len(motif)
    BS = plusLongSuffixePrefixe(motif)   #au pire on l'utilise...
    for j in range(m-1) :   #car BS[m-1]=1
        k = j
        while k >= 0 :
            if motif[j+1:] == motif[k:k+m-j-1] and  (k==0 or motif[j] != motif[k-1]) :
                #k==0 or  pour éviter le k-1 = -1 < 0.   dans ce cas, il n'y a pas de lettre qui précède...
                BS[j] = j-k+1
                break
            k -= 1
    return BS 


print(bonSuffixe('GCAGAGAG'))
#[7, 7, 7, 2, 7, 4, 7, 1]
print(bonSuffixe('ABABA'))
#[2, 2, 4, 4, 1]

#recherche textuelle avec cette heuristique du Bon Suffixe

def rechercheBSNbOp(texte, motif) :
    m = len(motif)
    n = len(texte)
    res = []
    comp = 0
    BS = bonSuffixe(motif)
    #boucle pour faire glisser le motif sous le texte à partir de zéro an faisant attention de ne pas dépasser ! 
    i = 0
    while i <= n-m :
        j = m - 1             #on commene à la fin du motif !
        while j >= 0 and texte[i+j] == motif[j] :   #on incrémente tant que c'est identique
            j -= 1
            comp += 1
        if j == -1 :          #motif trouvé!!
            res. append(i)
            i += BS[0]            
        else :
            i += BS[j]   
            comp += 1         #pour ne pas oublier de compter les échecs de comparaison (mismatch)
    return "Motif trouvé en " + str(comp) + ' comparaisons, en position(s) : ' + str(res)

alphabet = ["A", "C", "G", "T"]
print(rechercheBSNbOp(T,M))
# Motif trouvé en 17 comparaisons, en position(s) : [5]


################################################
##  Recherche de motifs exacts                ##
##    Boyer-Moore : mettre tout ça ensemble   ##
################################################

print('BM')

def recherche(texte, motif, sigma):
    m = len(motif)
    n = len(texte)
    res = []
    comp = 0
    MC = mauvaisCarac(motif, sigma)
    BS = bonSuffixe(motif)
    #boucle pour faire glisser le motif sous le texte à partir de zéro an faisant attention de ne pas dépasser ! 
    i = 0
    while i <= n-m :
        j = m - 1                                   #on commene à la fin du motif !
        while j >= 0 and texte[i+j] == motif[j] :   #on incrémente tant que c'est identique
            j -= 1
            comp += 1
        if j == -1 :          #motif trouvé!!
            res. append(i)
            i += BS[0]        #forcément meilleur que MC : ils sont bons !!        
        else :
            i += max(BS[j], MC[texte[i+j]] - m + 1 + j)    # décalage du motif le plus possible...
            comp += 1         #pour ne pas oublier de compter les échecs de comparaison (mismatch)
    return "Motif trouvé en " + str(comp) + ' comparaisons, en position(s) : ' + str(res)  

alphabet = ["A", "C", "G", "T"]
print(recherche(T,M,alphabet))
# Motif trouvé en 17 comparaisons, en position(s) : [5]
print()
print(recherche('CBABABA','ABABA',["A", "B", "C"]))
# Motif trouvé en 10 comparaisons, en position(s) : [2]


# #autres essais
# print()
# print()
# print()
# print('exemple1')
# chaine = 'GCATCGCAGAGAGTATACAGTACG'
# mot = 'GCAGAGAG'
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# print('texte : ',chaine)
# print('motif : ',mot)
# print(rechercheAlgoNaif(chaine, mot))
# print(recherche(chaine, mot, alphabet))
# print()
# print('exemple2')
# chaine = 'GGCAGCCGAACCGCAGCAGCAGCA'
# mot = 'AGC'
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# print('texte : ',chaine)
# print('motif : ',mot)
# print(rechercheAlgoNaif(chaine, mot))
# print(recherche(chaine, mot, alphabet))
# print()
# print('exemple3')
# chaine = 'GGCAGCCGAACCGCAGCAGCAGCA'
# mot = 'AGCA'
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# print('texte : ',chaine)
# print('motif : ',mot)
# print(rechercheAlgoNaif(chaine, mot))
# print(recherche(chaine, mot, alphabet))
# print()
# print('exemple4')
# chaine = 'CAATGTCTGCACCAAGACGCCGGCAGGTGCAGACCTTCGTTATAGGCGATGATTTCGAACCTACTAGTGGGTCTCTTAGGCCGAGCGGTTCCGAGAGATAGTGAAAGATGGCTGGGCTGTGAAGGGAAGGAGTCGTGAAAGCGCGAACACGAGTGTGCGCAAGCGCAGCGCCTTAGTATGCTCCAGTGTAGAAGCTCCGGCGTCCCGTCTAACCGTACGCTGTCCCCGGTACATGGAGCTAATAGGCTTTACTGCCCAATATGACCCCGCGCCGCGACAAAACAATAACAGTTT'
# mot = 'ACCTTCG'
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# print('texte : ',chaine)
# print('motif : ',mot)
# print(rechercheAlgoNaif(chaine, mot))
# print(recherche(chaine, mot, alphabet))



