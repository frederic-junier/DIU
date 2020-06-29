
# coding: utf-8

# ## Recherche naive par fenêtre glissante

# In[45]:


def correspondance_motif(texte, motif,i):
    """Recherche la correspondance de motif dans texte
    à partir de la position i"""
    if i + len(motif) > len(texte):
        return False
    for j in range(0, len(motif)):
        if motif[j] != texte[i + j]:
            return False
    return True

def recherche_motif_naive(texte, motif):
    """Retourne la position où le motif a été trouvé par fenetre glissante
    ou -1 si le motif ne se trouve pas dans le texte
    Si n = len(texte) et m = len(motif), la complexité est en O((n-m)*m)"""
    for i in range(len(texte) - len(motif) + 1):
        if correspondance_motif(texte, motif,i):
            return i
    return -1


# ## Algorithme de Boyer-Moore

# Sitographie :
#     
# * [https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm)
# * [http://whocouldthat.be/visualizing-string-matching/](http://whocouldthat.be/visualizing-string-matching/)

# ### Règle du mauvais caractère

# In[46]:


def mauvais_caractere(motif, alphabet):
    """Retourne un dictionnaire avec pour chaque caractère de l'alphabet, le nombre de décalage 
    à partir de la fin du motif avant de trouver ce caractère
    On ne compte pas la dernière lettre du motif et le décalage vaut m = len(motif)"
    si on ne trouve pas le caractère"""
    m = len(motif)
    #mc = [0] * len(alphabet)  
    mc = {c : 0 for c in alphabet} #j préfère utiliser un dictionnaire
    for i in range(len(alphabet)):
        c = alphabet[i]
        k = 1
        while k < m and c != motif[m - 1 - k]:
            k = k + 1
        mc[i] = k
    return mc


# In[47]:


mauvais_caractere('GCAGAGAG', 'ACGT')


# In[48]:


def correspondance_suffixe(motif, i, j):
    m = len(motif)
    if motif[j] != motif[i]:
        d = 1
        while  i + d < m and motif[j + d] == motif[i + d]:
            d += 1
        return i + d == m
    return False
        

def comparaison_prefixe_suffixe(debut_suffixe, motif):
    index_prefixe = 0
    index_suffixe = debut_suffixe
    m = len(motif)
    while index_suffixe < m and motif[index_suffixe] == motif[index_prefixe]:
        index_prefixe += 1
        index_suffixe += 1
    return index_suffixe == m
    
def bon_suffixe(motif):
    m = len(motif)
    bs = [0] * m   
    for i in range(m - 1, -1, -1):        
        j = i - 1        
        while j >= 0 and not correspondance_suffixe(motif, i, j):            
            j = j - 1   
        if j >= 0:  #second cas du bon suffixe : recherche du début d'un suffixe/préfixe 
            bs[i] = i - j           
        else:  # premier cas du bon suffixe : recherche du 
            p = i  + 1
            while p < m and not comparaison_prefixe_suffixe(p, motif):
                p = p + 1
            bs[i] = p
    return bs


# In[49]:


bon_suffixe('GCAGAGAG')


# In[50]:


bon_suffixe('ABABA')


# In[51]:


bon_suffixe('AAA')


# In[52]:


def boyer_moore(texte, motif, alphabet):
    #initialisation des longueurs
    n = len(texte)
    m = len(motif)
    #pré-traitement du motif
    bs = bon_suffixe(motif)
    mc = mauvais_caractere(motif, alphabet)
    print(bs, mc)
    #recherche du motif  dans le texte
    i = 0 #indice dans le texte
    while i <= n - m:
        j = m - 1  #on lit le motif de droite à gauche
        while j >= 0 and motif[j] == texte[i+j]:
            j = j - 1
        if j < 0:
            print(f"Motif trouvé en {i}")
            #décalage du motif
            i = i + bs[0]
        else:
            #décalage du motif
            i = i + max(bs[j], mc[texte[i+j]] + j - m + 1)
        


# In[53]:


texte = "GCATCGCAGAGAGTATACAGTACG"
motif = "GCAGAGAG"
alphabet = "ACGT"
boyer_moore(texte, motif, alphabet)


# In[54]:


T = "GCATCGCAGAGAGTATACAGTACG"
M = "GCAGAGAG"
alphabet = "ACGT"
boyer_moore(T, M, alphabet)


# In[55]:


bon_suffixe(M)

