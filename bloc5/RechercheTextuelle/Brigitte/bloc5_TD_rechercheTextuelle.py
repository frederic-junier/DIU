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
    i = 0
    while i < n-m+1 :
        j = 0
        while j <= m-1 and texte[i+j] == motif[j] :
            j += 1
        if j == m :
            res. append(i)
        if lettresDiff == False :
            i += 1
        else :  # on décale directement de j car on sait que motif[j-1] est ok et qu'on ne la retouve psa avt...
            i += max(1,j)    #pour éviter le cas j=0
    return "Motif trouvé en " + str(res)

def mauvaisCarac(motif, sigma) :
    """ renvoie le nombre de positions à remonter pour trouver la dernière occurence de chaque caractère
    de l'alphabet dans le motif à partir de la position m-1.
    Si non présent, renvoie m. Si en présent en m-1, on cherche l'occurence suivante"""
    s = len(sigma)
    m = len(motif)
    MC = [m]*s
    for i in range(m-1) :   #ainsi on se s'occupe pas de la lettre en m-1
        #au pire on écrase les valeurs des lettres qui ont plusieurs occurence en gardant la dernière valeur
        MC[sigma.index(motif[i])] = m - i-1   #le -1 c'est parce qu'on commence à zero
    return MC

#print(mauvaisCarac('GCAGAGAG', 'ACGT'))
# [1,6,2,8]

def plusLongSuffixePrefixe(motif) :
    """ renvoie l'indice du début du plus long suffixe qui est aussi préfixe dans le motif. 
    On interdit le mot entier. """
    m = len(motif)
    for p in range(1, m) :  #boucle avec rupture de flux sur p croissant car plus p est petit, plus le suffixe est long
        if motif[p:] == motif[:m-p] :
            return p
    return 1                #pour que l'on retourne 1 dans le pire des cas du bonSuffixe   

#print(plusLongSuffixePrefixe('GCAGAGAG'))
# 7

def bonSuffixe(motif):
    """ renvoie un tableau où la valeur d'index j est j-k-1 lorsqu'il existe k correspondant 
    à la plus grande position dans le motif où M[j+1..m-1]=[k..m-j-1] et [j]!=M[k-1]
    et lorsqu'il n'existe pas de k on met plusLongSuffixePrefixe(motif) ! """
    m = len(motif)
    pls = plusLongSuffixePrefixe(motif)
    BS = [1]*m   #au pire on décale seulement de 1
    for j in range(m-1) :
        k = 0
        while k < j+1 :
            if motif[j+1:] == motif[k:k+m-j-1] and  motif[j] != motif[k-1] :
                BS[j] = j-k+1
            else :
                if BS[j] == 1 :
                    BS[j] = pls
            k += 1
    return BS 

#print(bonSuffixe('GCAGAGAG'))
#[7, 7, 7, 2, 7, 4, 7, 1]

def recherche(texte, motif, sigma):
    m = len(motif)
    n = len(texte)
    MC = mauvaisCarac(motif, sigma)
    BS = bonSuffixe(motif)
    res = []
    i = 0
    while i <= n-m :
        j = m-1
        while j>=0 and motif[j] == texte[i+j] :
            j = j - 1
        if j < 0:
            res.append(i)
            i = i + BS[0]   # décalage du motif avec BS : on ne peut pas faire mauvais caractère car ils sont bons !! 
        else :
            i = i + max(BS[j] , MC[sigma.index(texte[i+j])]+j-m+1)    # décalage du motif le plus possible...
    return "Motif trouvé en " + str(res)

print()
print('exemple1')
chaine = 'GCATCGCAGAGAGTATACAGTACG'
mot = 'GCAGAGAG'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print('texte : ',chaine)
print('motif : ',mot)
print(rechercheAlgoNaif(chaine, mot))
print(recherche(chaine, mot, alphabet))
print()
print('exemple2')
chaine = 'GGCAGCCGAACCGCAGCAGCAGCA'
mot = 'AGC'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print('texte : ',chaine)
print('motif : ',mot)
print(rechercheAlgoNaif(chaine, mot))
print(recherche(chaine, mot, alphabet))
print()
print('exemple3')
chaine = 'GGCAGCCGAACCGCAGCAGCAGCA'
mot = 'AGCA'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print('texte : ',chaine)
print('motif : ',mot)
print(rechercheAlgoNaif(chaine, mot))
print(recherche(chaine, mot, alphabet))
print()
print('exemple4')
chaine = 'CAATGTCTGCACCAAGACGCCGGCAGGTGCAGACCTTCGTTATAGGCGATGATTTCGAACCTACTAGTGGGTCTCTTAGGCCGAGCGGTTCCGAGAGATAGTGAAAGATGGCTGGGCTGTGAAGGGAAGGAGTCGTGAAAGCGCGAACACGAGTGTGCGCAAGCGCAGCGCCTTAGTATGCTCCAGTGTAGAAGCTCCGGCGTCCCGTCTAACCGTACGCTGTCCCCGGTACATGGAGCTAATAGGCTTTACTGCCCAATATGACCCCGCGCCGCGACAAAACAATAACAGTTT'
mot = 'ACCTTCG'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
print('texte : ',chaine)
print('motif : ',mot)
print(rechercheAlgoNaif(chaine, mot))
print(recherche(chaine, mot, alphabet))



