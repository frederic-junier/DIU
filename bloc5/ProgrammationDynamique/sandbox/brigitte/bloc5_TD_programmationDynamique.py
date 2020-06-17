# ## Termes de la suite de Fibonacci
# 
# #solution recursive
# def fibonacci(n) :
#     if n == 0 or n == 1 :
#         return n
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)
# 
# #solution dynamique iteratif
# def fibonacciDyna(n) :
#     if n <= 1 :
#         return n
#     fibo = [0,1]
#     k = 2
#     while k <= n :
#         fibo.append(fibo[k-1] + fibo[k-2])
#         k += 1
#     return fibo[n]
# 
# #solution dynamique recursif
# def fibonacciMemo(n,mem) :
#     if n==0 :
#         return 0
#     elif mem[n]>0 :
#         return mem[n]
#     else:
#         mem[n] = fibonacciMemo(n-1,mem) + fibonacciMemo(n-2,mem)
#         return mem[n]
# 
# print(fibonacci(7))
# print(fibonacciDyna(7))
# mem = [0]*(100)
# mem[1] = 1
# print(fibonacciMemo(7,mem))
# print()
# 
# 
# ## Rendu de pièces de monnaire
# 
# # solution goutonne
# def renduMonnaieGlouton(montant) :
#     return renduMonnaieRecurGlouton(montant,[],len(systemeMonetaire)-1)
# 
# def renduMonnaieRecurGlouton(montant,rendu,indPiece) :
#     if montant == 0 :
#         return rendu
#     while montant >= systemeMonetaire[indPiece] :
#         montant -= systemeMonetaire[indPiece]
#         rendu.append(systemeMonetaire[indPiece])
#     return renduMonnaieRecurGlouton(montant,rendu,indPiece-1)
# 
# # solution recursive
# def renduMonnaieRecur(montant) :
#     #Renvoie le nombre minimal de pièces mais pas les valeurs
#     if montant == 0 :
#         return 0
#     nbPieces = montant//systemeMonetaire[0]
#     for piece in systemeMonetaire :
#         if montant - piece >= 0 :
#             nbPieces = min(nbPieces, 1 + renduMonnaieRecur(montant-piece))
#     return nbPieces
# 
# #sol de Fred... ???
# # def renduMonnaieRec(setReste, systeme,  nbpieces):
# #     setReste2 = set()
# #     for somme in setReste:
# #         for piece in systeme:
# #             if piece <= somme:
# #                 reste = somme - piece
# #                 if reste == 0:
# #                     return nbpieces + 1
# #                 setReste2.add(somme - piece)
# #     return renduMonnaieRec(setReste2, systeme, nbpieces + 1)
# 
# # solution dynamique version recursive
# def renduMonnaieDyna(montant):
#     #Renvoie le nombre minimal de pièces mais pas les valeurs
#     m = [0]*(montant+1)  #on veut renvoyer le b de pièces pour un toto allant de 0 à montant inclus.
#     return renduMonnaieRecurDyna(montant,m)
# 
# def renduMonnaieRecurDyna(montant,mem):
#     if montant==0:
#         return 0
#     elif mem[montant]>0:
#         return mem[montant]
#     else:
#         nbPieces = montant//systemeMonetaire[0]
#         for piece in systemeMonetaire :
#             if piece <= montant :
#                 nb = 1 + renduMonnaieRecurDyna(montant-piece,mem)
#                 if nb < nbPieces :
#                     nbPieces = nb 
#         mem[montant] = nbPieces
#     return mem[montant]
# 
# #Rendu dynamique version itérative
# def renduMonnaieIterDyna(montant) :
#     '''Renvoie le nombre minimal de pièces mais pas les valeurs'''
#     '''précondition : pièces dans l'ordre croissant'''
#     # Etape 1 - on décompose : on cherche à rendre 0,1,2,..montant  (montant +1 valeurs)
#     # avec différentes contraintes sur les pièces : pieces<= syst[0], pieces<= syst[1], ... (len(syst) contraintes différentes)
#     # on a donc (montant+1)*len(syst) problèmes différents.
#     # on décide de les représenter par une liste de len(syst) listes de (montant+1) nombres initialisé à zéro
#     # mem[i][m] contient le nombre minimal de pièces rendues pour le montant m avec des pièces <= syst[i]
#     mem = [[0]*(montant+1) for i in range(len(systemeMonetaire))]
#     # Etape 2 - on cherche à resoudre cas de base : rendre 0 est trivial mais pas besoin de changer car c'est l'initilisation
#     # de plus, on peut facilement écrire la liste qui correspond à rendre les montants avec un seul type de pièce !
#     for m in range(montant + 1) :
#         if m % systemeMonetaire[0] == 0 :
#             mem[0][m] = m // systemeMonetaire[0]    
#     # Etape 3 - on cherche une relation... : on va remplir de proche en proche en utilisant les problèmes pcdts.
#     # pour chaque liste mem[i], on peut déjà recopier les valeurs de la liste du dessus mem[i-1]
#     #    En effet, si on peut rendre la somme m avec au minimum mem[i-1][m] pièces <= syst[i-1]
#     #    on peut rendre la somme m avec au minimum mem[i-1][m] pièces <= syst[i] !!!
#     for i in range(1,len(systemeMonetaire)) : 
#         for m in range(montant + 1):
#             mem[i][m] = mem[i-1][m]
#     # et on regarde pour chaque valeur de la liste mem[i], de la plus petite à la plus grande,
#     # si on aurait utilisé moins de pièce en essayant de faire le montant k-syst[i] avec des pièces <= syst[i]
#     # en faisant attention que la piece ne dépasse pas le montant k à rendre !!
#             if systemeMonetaire[i] <= m : 
#                 if mem[i][m-systemeMonetaire[i]] + 1 < mem[i][m] :
#                     mem[i][m] = mem[i][m-systemeMonetaire[i]] + 1             
#     return mem[len(systemeMonetaire)-1][montant]
# 
# #Rendu dynamique version itérative
# def renduMonnaieIterDynaValeurs(montant) :
#     '''Renvoie le nombre minimal de pièces ET leurs valeurs'''
#     mem = [[0]*(montant+1) for i in range(len(systemeMonetaire))]
#     for m in range(montant + 1) :
#         if m % systemeMonetaire[0] == 0 :
#             mem[0][m] = m // systemeMonetaire[0]    
#     for i in range(1,len(systemeMonetaire)) : 
#         for m in range(montant + 1):
#             mem[i][m] = mem[i-1][m]
#             if systemeMonetaire[i] <= m : 
#                 if mem[i][m-systemeMonetaire[i]] + 1 < mem[i][m] :
#                     mem[i][m] = mem[i][m-systemeMonetaire[i]] + 1 
#     res = []
#     i = len(systemeMonetaire)-1
#     while i > 0 :
#         while mem[i-1][montant] - mem[i][montant] > 0 :
#             res.append(systemeMonetaire[i])
#             montant -= systemeMonetaire[i]
#         i -= 1
#     while montant > 0 :
#         res.append(systemeMonetaire[0])
#         montant -= systemeMonetaire[0]
#     return res
# 
# systemeMonetaire = [1,7,23]     #système non canonique = non optimal pour l'algo glouton
# M = 28
# print(systemeMonetaire, M)
# print('Glouton ',renduMonnaieGlouton(M))
# print('Nb pièces, recursif ',renduMonnaieRecur(M))
# print('Nb pièces, dyna, rec ',renduMonnaieDyna(M))
# print('Nb pièces, dyna, iter ',renduMonnaieIterDyna(M))
# print('Listes pièces, dyna, iter ',renduMonnaieIterDynaValeurs(M))
# print()
# systemeMonetaire = [1,2,5,10,50,100]    #système canonique = optimal pour l'algo glouton!!
# M = 171
# print(systemeMonetaire, M)
# print('Glouton ',renduMonnaieGlouton(M))
# #print('Nb pièces, recursif ',renduMonnaieRecur(M))
# print('Nb pièces, dyna ',renduMonnaieDyna(M))
# print('Nb pièces, dyna, iter ',renduMonnaieIterDyna(M))
# print('Listes pièces, dyna, iter ',renduMonnaieIterDynaValeurs(M))
# print()
# systemeMonetaire = [1,2,5,10,20,50,100,200]  #système canonique = optimal pour l'algo glouton!!
# M = 263
# print(systemeMonetaire, M)
# print('Glouton ',renduMonnaieGlouton(M))
# #print('Nb pièces, recursif ',renduMonnaieRecur(M))
# print('Nb pièces, dyna ',renduMonnaieDyna(M))
# print('Nb pièces, dyna, iter ',renduMonnaieIterDyna(M))
# print('Listes pièces, dyna, iter ',renduMonnaieIterDynaValeurs(M))
# print()
# systemeMonetaire = [1,3,4]  #système non canonique = non optimal pour l'algo glouton
# M = 6
# print(systemeMonetaire, M)
# print('Glouton ',renduMonnaieGlouton(M))
# print('Nb pièces, recursif ',renduMonnaieRecur(M))
# print('Nb pièces, dyna ',renduMonnaieDyna(M))
# print('Nb pièces, dyna, iter ',renduMonnaieIterDyna(M))
# print('Listes pièces, dyna, iter ',renduMonnaieIterDynaValeurs(M))
# print()
# 
# 


## Le sac  à dos

# solution goutonne
def sacADos(capacite) :
    poidsActuel = 0
    solution = []
    for i in range(len(listeObjets)) :
        if poidsActuel + listeObjets[i][2] <= capacite :
            poidsActuel += listeObjets[i][2]
            solution.append(listeObjets[i][0])
    return solution

# solution dynamique iterative
def sacADosDynaTab(capacite) :
    # Ecrire la fonction qui permet de créer/remplir max_val et optimal et qui retourne le tableau optimal.
    # elle prend la capacité du sac en paramètre et affecte chaque case en utilisant le principe d’optimalité du problème.
     
    # Etape 1 - on décompose :
    # max_val aura capacité+1 lignes (pour le poids du sac de 0 à capacite)
    # chaque ligne aura nb_objets + 1 colonnes
    # on a lig0 et col0 qui n'ont QUE des zeros !!
    # max_val[i][j] est la valeur max pour une capacité de i avec les j premiers objets 
    max_val = [[0]*(len(listeObjets)+1) for i in range(capacite+1)]
    # optimal sera de même dimension
    optimal = [[0]*(len(listeObjets)+1) for i in range(capacite+1)]
    # Etape 2 - on cherche à resoudre cas de base :
    # On remplit la première colonne de max_val et on remplit en meme temps celle du tableau optimal
    for i in range(1,capacite+1) :
       if i >= listeObjets[0][2] :            # si le poids de l'objet 1 (L[0][2]) est sup à la capacité du sac
           max_val[i][1] = listeObjets[0][1]  # alors on note la valeur correspondante de cet unique objet dans la première colonne non nulle 
           optimal[i][1] = 1  # l’objet 0 fait partie de la configuration optimale courante à partir de son propre poids
    # Etape 3 - on cherche une relation...
    # attention : on va remplir les tableau max_val et optimal colonne par colonne
    for j in range(2, len(listeObjets)+1) :
        poids = listeObjets[j-1][2]
        valeur = listeObjets[j-1][1]
        for i in range(1,capacite+1) : 
            if i - poids >= 0 :
                if max_val[i][j-1] < max_val[i-poids][j-1]+valeur :
                    max_val[i][j] = max_val[i-poids][j-1]+valeur
                    optimal[i][j] = 1    # signifie que l’objet j fait alors partie de la configuration optimale courante
                else :
                    max_val[i][j] = max_val[i][j-1]
            else :
                max_val[i][j] = max_val[i][j-1]
            #print(max_val[i][j])
    for lig in max_val :
        print(lig)
    print()
    for lig in optimal :
        print(lig)
    return optimal

def sacADosDyna(capacite) :
    # Ecrire la fonction qui retourne la liste des objets de valeur optimale pour un poids donné en paramètre.
    res = []
    tab = sacADosDynaTab(capacite)
    j = len(listeObjets)
    i = capacite
    while i>0 and j > 0:       
        while tab[i][j] != 1 :
            j -= 1                 
        res.append(listeObjets[j-1][0])
        i -= listeObjets[j-1][2]
        j -= 1
    res.reverse()
    return res

W = 6
listeObjets = [['A',6,5], ['B',3,2], ['C',3,2], ['D',3,2], ['E',1,1]]
#Objets sous la forme : nom/valeur/poids par ordre décroissant de valeur
print('liste de objets : ', listeObjets)
print('poids du sac : ',W)
print('solution gloutonne ', sacADos(W))
print('solution optimale :', sacADosDyna(W))
print()
W = 9
listeObjets = [['A',6,5], ['B',3,2], ['C',3,2], ['D',3,2], ['E',1,1]]
#Objets sous la forme : nom/valeur/poids par ordre décroissant de valeur
print('liste de objets : ', listeObjets)
print('poids du sac : ',W)
print('solution gloutonne ', sacADos(W))
print('solution optimale :', sacADosDyna(W))
print()
W = 12
listeObjets = [['A',6,5], ['B',3,2], ['C',3,2], ['D',3,2], ['E',1,1]]
#Objets sous la forme : nom/valeur/poids par ordre décroissant de valeur
print('liste de objets : ', listeObjets)
print('poids du sac : ',W)
print('solution gloutonne ', sacADos(W))
print('solution optimale :', sacADosDyna(W))
