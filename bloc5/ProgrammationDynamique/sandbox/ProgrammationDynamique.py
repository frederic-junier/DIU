
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
# 
# 
# 
# Les algorithmes utilisant le principe de mémoïsation forment un sous-ensemble des algorithmes dit de programmation dynamique. La programmation dynamique consiste à résoudre un problème soit à l'aide d'un algorithme (souvent itératif) ascendant (ou bottom-up) en stockant des données déjà calculées (souvent dans un tableau) et utilise directement la sous-structure optimale du problème, soit à l'aide d'un algorithme (souvent récursif) descendant (ou top-down) qui utilise le principe de mémoïsation de ces données (c-à-d qui teste si on a déjà calculé les données et ne le refait pas le cas échéant).

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

# In[62]:


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


# In[63]:


[fiboDyna(n) == fibonacci(n) for n in range(10)]


# ### Comparaison de performances

# In[64]:


import timeit


# In[65]:


timeit.timeit(lambda : [fibonacci(n) for n in range(30)], number = 10)/10


# In[66]:


timeit.timeit(lambda : [fiboDyna(n) for n in range(30)], number = 10)/10


# ## Rendu de pièces de monnaire

# Sitographie :
#     
# * Voir cet article [https://tryalgo.org/fr/2016/12/11/rendudemonnaie/](https://tryalgo.org/fr/2016/12/11/rendudemonnaie/)
# * Voir le document d'accompagnement [https://cache.media.eduscol.education.fr/file/NSI/76/4/RA_Lycee_G_NSI_algo-gloutons_1170764.pdf](https://cache.media.eduscol.education.fr/file/NSI/76/4/RA_Lycee_G_NSI_algo-gloutons_1170764.pdf)

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

# In[67]:


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


# In[68]:


#Rendu dynamique version itérative

def renduMonnaieDynaIter(montant, systeme, verbose = False):
    pieces_min = [ [0] * len(systeme) for _ in range(montant + 1)]
    for m in range(1, montant + 1):
        if m % systeme[0] == 0:
            pieces_min[m][0] = m // systeme[0]
        else:
            pieces_min[m][0] = 0
        for indexpiece in range(1, len(systeme), systeme[0]):
            if systeme[indexpiece] <= m:
                pieces_min[m][indexpiece] = min(1 + pieces_min[m - systeme[indexpiece]][indexpiece], pieces_min[m][indexpiece - 1])
            else:
                pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1]
    if verbose:
        print(pieces_min)
    return pieces_min[montant][-1]


# In[69]:


#Rendu dynamique version itérative avec traçage des pièces rendues

def renduMonnaieDynaIterDetail(montant, systeme, verbose = False):
    """Une version Bottom -> Top"""
    pieces_min = [ [[0, 0] for _ in range(len(systeme))] for _ in range(montant + 1)]
    for m in range(1, montant + 1, systeme[0]):
        if m % systeme[0] == 0:
            pieces_min[m][0] = [m // systeme[0], systeme[0]]
        else:
            pieces_min[m][0] = [0, systeme[0]]
        for indexpiece in range(1, len(systeme)):
            if systeme[indexpiece] <= m:
                p = m - systeme[indexpiece]
                if 1 + pieces_min[p][indexpiece][0] < pieces_min[m][indexpiece - 1][0]:
                    #nb minimal de pieces rendues pour un montant m avec des pieces d'index <= indexpiece
                    pieces_min[m][indexpiece][0] = 1 + pieces_min[p][indexpiece][0]   
                    #valeur de la dernière pièce rendue
                    pieces_min[m][indexpiece][1] = systeme[indexpiece]
                else:
                    pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1]
            else:
                pieces_min[m][indexpiece] = pieces_min[m][indexpiece - 1]
    if verbose:
        print(pieces_min)
    nbpieceMin = pieces_min[montant][-1][0]    
    dernierePiece = pieces_min[montant][-1][1]
    reste = montant - dernierePiece
    rendu = [dernierePiece]
    while reste > 0:
        dernierePiece = pieces_min[reste][-1][1]
        reste = reste - dernierePiece
        rendu.append(dernierePiece)
    return rendu


# In[70]:


systemeMonetaireCanonique = [1,2,5,10,20,50,100,200]  #système canonique, optimal également pour l'algo glouton
print(renduMonnaieGlouton(263,systemeMonetaireCanonique))
print(renduMonnaieDynaIterDetail(263, systemeMonetaireCanonique))


# In[71]:


systemeMonetaireNonCanonique = [1,3, 4]  
print(renduMonnaieGlouton(6,systemeMonetaireNonCanonique))
print(renduMonnaieDynaIter(6, systemeMonetaireNonCanonique, verbose = True))
print(renduMonnaieDynaIterDetail(6, systemeMonetaireNonCanonique))


# In[72]:


systemeMonetaireNonCanonique = [1,7, 23]  
print(renduMonnaieGlouton(28,systemeMonetaireNonCanonique))
print(renduMonnaieDynaIterDetail(28, systemeMonetaireNonCanonique))


# In[73]:


#rendu de monnaie version récursive (mais pas dynamique)

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


# In[74]:


renduMonnaieRec({263}, [1,2,5,10,20,50,100,200], 0)


# In[75]:


renduMonnaieRec({28}, [1,7, 23], 0)


# In[76]:


renduMonnaieRec({6}, [1,3, 4], 0)


# In[77]:


#Décorateur pour compter les appels

def counter(f):

    def wrap(*args, **kwargs):
        wrap.compteur += 1
        rep = f(*args, **kwargs)         
        return rep
    
    #compteur attaché dans la 'closure' de  la fonction wrap comme attribut
    #c'est plus facile pour y accéder de l'extérieur
    wrap.compteur = 0    
    return wrap
    


# In[78]:


def renduMonnaieDynaRec(somme, systeme):
    
    """Une version Top-> Bottom, dynamique récursive, avec liste des pièces du rendu"""
    
    memo = [[(0, None, None) for _ in range(len(systeme))] for _ in range(somme + 1)]
    #memo[montant][indexpiece] contiendra le nb de pieces minimal calculé,
    #la somme restante et le plus grand index de piece utilisé pour le rendu
  
    @counter
    def aux(somme, indexpiece):
        """Complexite spatiale en O(montant * len(systeme)) la même que pour la version Bottom -> Top"""        
        if somme == 0:
            return (0, None, None)
        if memo[somme][indexpiece][0] > 0:
            return memo[somme][indexpiece]
        if indexpiece == 0:
            if somme % systeme[0] == 0:
                q = somme // systeme[0]
                memo[somme][indexpiece] = (q, 0, 0)
                return (q, 0, 0)
            memo[somme][indexpiece] = (0, None,None)
            return (0, None, None)   
        v1, m1, i1 = aux(somme, indexpiece - 1)
        if systeme[indexpiece] <= somme:
            v2, m2, i2 = aux(somme - systeme[indexpiece], indexpiece)
            v = v2 + 1
            if v < v1:                
                memo[somme][indexpiece] = (v, somme - systeme[indexpiece], indexpiece)
                return (v, somme - systeme[indexpiece], indexpiece)
        memo[somme][indexpiece] = v1, m1, i1
        return (v1, m1, i1)
    
   
    
    #print(memo)
    indexpiece = len(systeme) - 1
    aux(somme, indexpiece)
    print(f"{aux.compteur} appels récursifs")
    nbpiecemin, reste, indexpiece= memo[somme][indexpiece]
    dernierepiece = somme - reste
    rendu = []
    rendu.append(dernierepiece)
    somme = reste
    while somme > 0:
        _, reste, indexpiece= memo[somme][indexpiece]
        dernierepiece = somme - reste
        rendu.append(dernierepiece)
        somme = reste     
    return nbpiecemin, rendu


# In[79]:


renduMonnaieDynaRec(263, [1,2,5,10,20,50,100,200])


# In[80]:


renduMonnaieDynaRec(6, [1,3, 4])


# In[81]:


renduMonnaieDynaRec(28, [1,7, 23])


# In[82]:


renduMonnaieDynaRec(280, [1,7, 23])


# In[83]:


@counter
def renduMonnaieRecurDynaBrigitte(montant,mem):
    """Complexité spatiale en O(montant)"""
    if montant==0:
        return 0
    elif mem[montant]>0:
        return mem[montant]
    else:
        nbPieces = montant//systemeMonetaire[0]
        for piece in systemeMonetaire :
            if piece <= montant :
                nb = 1 + renduMonnaieRecurDynaBrigitte(montant-piece,mem)
                if nb < nbPieces :
                    nbPieces = nb 
        mem[montant] = nbPieces
    return mem[montant]

systemeMonetaire = [1,2,5,10,20,50,100,200]
print(f"Rendu min pour 263 avec systeme={systemeMonetaire} en {renduMonnaieRecurDynaBrigitte(263, [0] * (263+1))} pièces")
print(f"{renduMonnaieRecurDynaBrigitte.compteur} appels récursifs et somme * len(systeme) = {263 * len(systemeMonetaire)}")
renduMonnaieRecurDynaBrigitte.compteur = 0
systemeMonetaire = [1,7, 23]
print(f"Rendu min pour 280 avec systeme={systemeMonetaire} en {renduMonnaieRecurDynaBrigitte(280, [0] * (280+1))} pièces")
print(f"{renduMonnaieRecurDynaBrigitte.compteur} appels récursifs et somme * len(systeme) = {280 * len(systemeMonetaire)}")
renduMonnaieRecurDynaBrigitte.compteur = 0
print(f"Rendu min pour 280 avec systeme={systemeMonetaire} en {renduMonnaieRecurDynaBrigitte(28, [0] * (28+1))} pièces")
print(f"{renduMonnaieRecurDynaBrigitte.compteur} appels récursifs et somme * len(systeme) = {28 * len(systemeMonetaire)}")
renduMonnaieRecurDynaBrigitte.compteur = 0
systemeMonetaire = [1,3, 4]
print(f"Rendu min pour 6 avec systeme={systemeMonetaire} en {renduMonnaieRecurDynaBrigitte(6, [0] * (6+1))} pièces")
print(f"{renduMonnaieRecurDynaBrigitte.compteur} appels récursifs et somme * len(systeme) = {6 * len(systemeMonetaire)}")


# ## Le sac  à dos

# Sitographie :
# 
# * Voir l'article  de Wikipedia (partie sur la programmation dynamique) : [https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_sac_%C3%A0_dos#Programmation_dynamique](https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_sac_%C3%A0_dos#Programmation_dynamique)
# * Article plus abordable d'Interstices avec une applet : [https://interstices.info/le-probleme-du-sac-a-dos/](https://interstices.info/le-probleme-du-sac-a-dos/)

# ![sac à dos dynamique](sac_a_dos_dynamique.png)

# In[84]:


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


# In[85]:


sacDosDyna(9, [[6,5], [3,2], [3,2], [3,2], [1,1]])


# In[86]:


sacDosDyna(12, [[6,5], [3,2], [3,2], [3,2], [1,1]])

