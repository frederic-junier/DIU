
# coding: utf-8

# ## Recherche naive par fenêtre glissante

# In[41]:


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

# ### Règle du mauvais caractère

# In[60]:


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


# In[61]:


mauvais_caractere('GCAGAGAG', 'ACGT')


# In[53]:


def correspondance_suffixe(motif, i, j):
    m = len(motif)
    if motif[j] != motif[i]:
        d = 1
        while  i + d < m and motif[j + d] == motif[i + d]:
            d += 1
        return i + d == m
    return False
        


def bon_suffixe(motif):
    m = len(motif)
    bs = [0] * m   
    for i in range(m - 1, -1, -1):        
        j = i - 1        
        while j >= 0 and not correspondance_suffixe(motif, i, j):            
            j = j - 1   
        if j < 0:
            #second cas : recherche du plus long préfixe qui est aussi un suffixe
            p = i  + 1
            while p < m and motif[p] != motif[0]:
                p = p + 1
            debut_suffixe = p
            k = 0
            while p < m and motif[p] == motif[k]:
                p += 1
                k += 1
            if p == m and debut_suffixe < m:
                bs[i] = debut_suffixe
            else:
                bs[i] = m          
        else:
            bs[i] = i - j
    return bs


# In[54]:


bon_suffixe('GCAGAGAG')


# In[55]:


bon_suffixe('ABABA')


# In[56]:


bon_suffixe('AAA')


# In[58]:


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
        


# In[62]:


texte = "GCATCGCAGAGAGTATACAGTACG"
motif = "GCAGAGAG"
alphabet = "ACGT"
boyer_moore(texte, motif, alphabet)

