
# coding: utf-8

# # PROGRAMMATION DYNAMIQUE
# 
# 
# Nous avons vu pour la fonction de calcul de la somme maximale des valeurs d’une branche d’un arbre que la
# programmation dynamique permet de trouver une solution optimale là où un algorithme glouton ne la trouve pas
# forcément. La programmation dynamique consiste à résoudre un problème en le décomposant en sous-problèmes,
# puis à résoudre les sous-problèmes, des plus petits aux plus grands en stockant les résultats intermédiaires et en suivant une règle d’optimalité.
# 
# La méthode de programmation dynamique, comme la méthode diviser-pour-régner, résout des problèmes en
# combinant des solutions de sous-problèmes. Les algorithmes diviser-pour-régner partitionnent le problème en
# sous-problèmes indépendants qu’ils résolvent récursivement, puis combinent leurs solutions pour résoudre le
# problème initial. Mais la méthode diviser-pour-régner est inefficace si on doit résoudre plusieurs fois le même
# sous-problème. En programmation dynamique, on se rappelle des sous-problèmes que l’on a résolus et de leurs
# solutions.

# # Termes de la suite de Fibonacci

# Rappellez vous de la fonction ci-dessous de calcul du n ème terme de la suite de Fibonacci où un appel récursif avec
# $n-1$ et $n-2$ entraînait une complexité en $O\left( \left(\frac{1+\sqrt{5}}{2} \right)^{n}\right)$.
# 
# 
# ~~~python
# def fibonacci (n):
#     if n == 0 or n == 1:
#         return n
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)
# ~~~

# Pour calculer le n ème terme on a besoin du n-1 qui lui-même à besoin du n-2 et n-3, qui seront réutilisés pour le n-2
# du n ème terme, etc. Il y a donc beaucoup de calculs dupliqués qui pourraient être évités. La solution est de ne les
# calculer que s’ils ne l’ont pas encore été.

# In[43]:


def fibonacci (n):
    if n == 0 or n == 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fiboDyna(n):
    
    def aux(n , t):
        if n <= 1:
            return t[n]
        if t[n] < 0:
            res = aux(n - 1, t ) + aux(n - 2, t )
            t[n] = res
            return res
        return t[n]
    
    return aux(n, [0,1] + [-1] * n)        


# In[39]:


[fiboDyna(n) == fibonacci(n) for n in range(10)]


# ### Comparaison de performances

# In[41]:


import timeit


# In[53]:


timeit.timeit(lambda : [fibonacci(n) for n in range(30)], number = 10)/10


# In[52]:


timeit.timeit(lambda : [fiboDyna(n) for n in range(30)], number = 10)/10


# ## Rendu de pièces de monnaire

# Nous avons vu précédement un algorithme glouton pour résoudre le problème du rendu de pièces de monnaie. La
# méthode employée était de toujours choisir la pièce de valeur la plus grande possible (afin de se rapprocher de
# zéro le plus rapidement possible). Nous avons vu que cet algorithme est efficace mais ne rend pas forcément la
# solution optimale.
# 
# ~~~python
# systemeMonetaire = [1,2,5,10,20,50,100,200] # exemple de liste de pièces
# def renduMonnaie(montant) :
#     return renduMonnaieRecur(montant,[], len(systemeMonetaire)-1)
# 
# def renduMonnaieRecur(montant,rendu,indPiece) :
#     if montant == 0 :
#         return rendu
#     while montant >= systemeMonetaire[indPiece]:
#         montant -= systemeMonetaire[indPiece]
#         rendu.append(systemeMonetaire[indPiece])
#     return renduMonnaieRecur(montant,rendu,indPiece-1)
# ~~~

# ![rendu monnaie](rendu-monnaie-dynamique.png)

# Ecrire une fonction Python qui prend en paramètre le montant à rendre et qui retourne la liste des pièces à rendre
# suivant le principe de la programmation dynamique. Le système monétaire sera connu et stocké sous la forme
# d’une liste de valeurs triées par ordre croissant.
# 
# Indication : Vous pourrez commencer par écrire une fonction qui crée et retourne un tableau à deux dimensions
# pieces_min tel que pieces_min[i][j] contient le nombre minimal de pièces pour un rendu de j centimes avec des
# pièces de valeur inférieure ou égale à celle de la i ème plus petite pièce du système monétaire.

# In[148]:


#Glouton

systemeMonetaire = [1,2,5,10,20,50,100,200] # exemple de liste de pièces

def renduMonnaieGlouton(montant, systemeMonetaire):
    return renduMonnaieRecurGlouton(montant,systemeMonetaire, [], len(systemeMonetaire)-1)

def renduMonnaieRecurGlouton(montant,systemeMonetaire, rendu,indPiece) :
    if montant == 0 :
        return rendu
    while montant >= systemeMonetaire[indPiece]:
        montant -= systemeMonetaire[indPiece]
        rendu.append(systemeMonetaire[indPiece])
    return renduMonnaieRecurGlouton(montant,systemeMonetaire, rendu,indPiece-1)


# In[159]:


#Rendu dynamique version itérative

def renduMonnaieDynaIter(montant, systeme):
    pieces_min = [ [0] * len(systeme) for _ in range(montant + 1)]
    for m in range(1, montant + 1):
        pieces_min[m][0] = m
        for indexpiece in range(1, len(systeme), systeme[0]):
            if systeme[indexpiece] <= m:
                pieces_min[m][indexpiece] = min(1 + pieces_min[m - systeme[indexpiece]][indexpiece], pieces_min[m][indexpiece - 1])
            else:
                pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1]
    return pieces_min[montant][-1]


# In[161]:


#Rendu dynamique version itérative avec traçage des pièces rendues

def renduMonnaieDynaIterDetail(montant, systeme):
    pieces_min = [ [[0, 0] for _ in range(len(systeme))] for _ in range(montant + 1)]
    for m in range(1, montant + 1, systeme[0]):
        pieces_min[m][0] = [m, systeme[0]]
        for indexpiece in range(1, len(systeme)):
            if systeme[indexpiece] <= m:
                p = m - systeme[indexpiece]
                if 1 + pieces_min[p][indexpiece][0] < pieces_min[m][indexpiece - 1][0]:
                    #nb minimal de pieces rendues pour un montant m avec des pieces d'index <= indexpiece
                    pieces_min[m][indexpiece][0] = 1 + pieces_min[p][indexpiece][0]   
                    #valeur de la dernière pièce rendue
                    pieces_min[m][indexpiece][1] = systeme[indexpiece]
                else:
                    pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1][:]
            else:
                pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1][:]
    nbpieceMin = pieces_min[montant][-1][0]    
    dernierePiece = pieces_min[montant][-1][1]
    reste = montant - dernierePiece
    rendu = [dernierePiece]
    while reste > 0:
        dernierePiece = pieces_min[reste][-1][1]
        reste = reste - dernierePiece
        rendu.append(dernierePiece)
    return rendu


# In[141]:


systemeMonetaireCanonique = [1,2,5,10,20,50,100,200]  #système canonique, optimal également pour l'algo glouton
print(renduMonnaieGlouton(263,systemeMonetaireCanonique))
print(renduMonnaieDynaIterDetail(263, systemeMonetaireCanonique))


# In[151]:


systemeMonetaireNonCanonique = [1,3, 4]  #système canonique, optimal également pour l'algo glouton
print(renduMonnaieGlouton(6,systemeMonetaireNonCanonique))
print(renduMonnaieDynaIterDetail(6, systemeMonetaireNonCanonique))


# In[150]:


systemeMonetaireNonCanonique = [1,7, 23]  #système canonique, optimal également pour l'algo glouton
print(renduMonnaieGlouton(28,systemeMonetaireNonCanonique))
print(renduMonnaieDynaIterDetail(28, systemeMonetaireNonCanonique))


# In[2]:


#rendu de monnaie dynamique version récursive

def renduMonnaieRec(setReste, systeme,  nbpieces):
    setReste2 = set()
    for somme in setReste:
        for piece in systeme:
            if piece <= somme:
                reste = somme - piece
                if reste == 0:
                    return nbpieces + 1
                setReste2.add(somme - piece)
    return renduMonnaieRec(setReste2, systeme, nbpieces + 1)          


# In[3]:


renduMonnaieRec({263}, [1,2,5,10,20,50,100,200], 0)


# In[4]:


renduMonnaieRec({28}, [1,7, 23], 0)


# In[5]:


renduMonnaieRec({6}, [1,3, 4], 0)


# ## Le sac  à dos

# Voir l'article  de Wikipedia (partie sur la programmation dynamique) : [https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_sac_%C3%A0_dos#Programmation_dynamique](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_sac_%C3%A0_dos#Programmation_dynamique)

# ![sac à dos dynamique](sac_a_dos_dynamique.png)

# In[72]:


def afficher_tab(tab, message):
    print(message)
    for ligne in tab:
        print(ligne)

def sacDosDyna(cap_sac, objet):
    nb_objet = len(objet)
    #j'ai mis des sentinelles
    max_val = [[0] * (cap_sac + 1) for _ in range(nb_objet  + 1)]
    optimal = [[0] * (cap_sac + 1) for _ in range(nb_objet  + 1)]
    for k in range(1, nb_objet + 1):
        for cap in range(1, cap_sac + 1):
            valeur = objet[k-1][0] 
            poids = objet[k-1][1] 
            if poids <= cap:
                max_avant = max_val[k-1][cap]
                valeur_avec = max_val[k-1][cap - poids]+ valeur
                if max_avant < valeur_avec:
                    max_val[k][cap] = valeur_avec
                    optimal[k][cap] = 1
                else:
                     max_val[k][cap] = max_avant
    valeur_max = max_val[nb_objet][cap_sac]
    liste_objets_max = []
    cap = cap_sac
    afficher_tab(max_val, "affichage de max_val")
    afficher_tab(optimal, "affichage de optimal")
    #décalage d'index entre max_val et objet à causes de sentinelles
    index_objet = nb_objet - 1
    while index_objet > 0:
        while index_objet > 0 and optimal[index_objet][cap] != 1:
            index_objet = index_objet - 1
        if index_objet > 0:
            cap = cap - objet[index_objet - 1][1]
            liste_objets_max.append(objet[index_objet - 1])      
    return (max_val[nb_objet][cap_sac], liste_objets_max)


# In[70]:


sacDosDyna(9, [[6,5], [3,2], [3,2], [3,2], [1,1]])


# In[71]:


sacDosDyna(12, [[6,5], [3,2], [3,2], [3,2], [1,1]])

