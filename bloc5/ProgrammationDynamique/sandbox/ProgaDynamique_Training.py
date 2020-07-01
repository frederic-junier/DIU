
# coding: utf-8

# ## Rendu de pièces de monnaie

# In[11]:


def rendu_monnaie_dyna(montant, systeme):
    pieces_min = [ [float('inf')] * (montant + 1)  for j in range(len(systeme))]
    for i in range(len(systeme)):
        pieces_min[i][0] = 0
    for j in range(1, montant + 1): 
        if j % systeme[0] == 0:
            pieces_min[0][j] = j // systeme[0]
        for i in range(1, len(systeme)):
            if systeme[i] <= j:
                pieces_min[i][j] = min(pieces_min[i-1][j], 1 + pieces_min[i][j-systeme[i]])
            else:
                pieces_min[i][j] = pieces_min[i-1][j]
    return (pieces_min, pieces_min[-1][montant])           


# In[7]:


rendu_monnaie_dyna(263, [1,2,5,10,20,50,100,200])


# In[31]:


def liste_rendu_monnaie_dyna(montant, systeme):
    pieces_min, _ = rendu_monnaie_dyna(montant, systeme)
    liste_rendu = []
    reste = montant
    (i, j) = (len(systeme) - 1, montant)
    while reste > 0:
        #on prend la plus grosse pièce
        if j-systeme[i] >= 0 and 1 + pieces_min[i][j-systeme[i]] < pieces_min[i-1][j]:
            (i, j) = (i, j-systeme[i])
            reste = reste - systeme[i]
            liste_rendu.append(systeme[i])
        #on ne prend pas la plus grosse pièce
        elif i > 0:
            (i, j) = (i - 1, j)  
        #il ne reste pas de plus petite pièce on est obligé de la prendre
        else:
            reste = reste - pieces_min[0][j]
            liste_rendu.append(pieces_min[0][j])
    return liste_rendu        


# In[30]:


liste_rendu_monnaie_dyna(263, [1,2,5,10,20,50,100,200])


# In[50]:


def rendu_monnaie_dyna_bfs(montant, systeme):
    file = [montant]
    nbpieces = 0
    while len(file) > 0:
        montant = file.pop()
        nbpieces += 1
        deja_calcule = [False] * (montant + 1)
        for i in range(0, len(systeme)):
            if systeme[i] <= montant:
                reste = montant - systeme[i]
                if not deja_calcule[reste]:
                    file.append(reste)
                    deja_calcule[reste] = True
                    if reste == 0:
                        return nbpieces
    return float('inf') #aucun rendu possible     


# In[51]:


rendu_monnaie_dyna_bfs(263, [1,2,5,10,20,50,100,200])


# In[57]:


def liste_rendu_monnaie_dyna_bfs(montant, systeme):
    file = [montant]
    nbpieces = 0
    memo_liste = {m : [] for m in range(montant + 1)}
    while len(file) > 0:
        montant = file.pop()
        nbpieces += 1
        deja_calcule = [False] * (montant + 1)
        for i in range(0, len(systeme)):
            if systeme[i] <= montant:
                reste = montant - systeme[i]
                if not deja_calcule[reste]:
                    file.append(reste)
                    deja_calcule[reste] = True
                    memo_liste[reste] = memo_liste[montant] + [systeme[i]]
                    if reste == 0:
                        return (nbpieces, memo_liste[0])
    return (float('inf'), []) #aucun rendu possible    


# In[58]:


liste_rendu_monnaie_dyna_bfs(263, [1,2,5,10,20,50,100,200])


# ## Le sac à dos

# In[69]:


def sac_dos_dyna(capacite_sac, objets):
    max_val = [ [0] * (capacite_sac + 1)  for j in range(len(objets) + 1)]
    optimal = [ [False] * (capacite_sac + 1)  for j in range(len(objets) + 1)]
    for i in range(len(objets)):
        max_val[i][0] = 0
    for capacite in range(1, capacite_sac + 1): 
        for i in range(len(objets)): 
            if objets[i][2] <= capacite:
                #on prend l'objet d'index i (ligne i + 1 dans max_val)
                if max_val[i][capacite - objets[i][2]] + objets[i][1]  > max_val[i][capacite]:
                    max_val[i + 1][capacite] = max_val[i][capacite - objets[i][2]] + objets[i][1]
                    optimal[i + 1][capacite] = True
                else:
                    max_val[i + 1][capacite] = max_val[i][capacite]
    return (max_val, optimal)           


# In[70]:


sac_dos_dyna(6, [['A', 6, 5], ['B', 3, 2], ['C', 3, 2], ['D', 3, 2], ['E',1,1]] )


# In[75]:


def liste_objets_sac_dos_dyna(capacite_sac, objets):
    max_val, optimal = sac_dos_dyna(capacite_sac, objets)
    index_objet = len(objets)
    capacite_restante = capacite_sac
    choix = []
    while index_objet > 0:
        if optimal[index_objet][capacite_restante]:
            if max_val[index_objet - 1][capacite_restante - objets[index_objet - 1][2]] + objets[index_objet - 1][1]  > max_val[index_objet - 1][capacite_restante]:
                choix.append( objets[index_objet - 1][0])
                (capacite_restante, index_objet) = (capacite_restante - objets[index_objet - 1][2], index_objet - 1)                
        else:
            index_objet -= 1    
    return choix


# In[76]:


liste_objets_sac_dos_dyna(6, [['A', 6, 5], ['B', 3, 2], ['C', 3, 2], ['D', 3, 2], ['E',1,1]] )

