
# coding: utf-8

# In[66]:


import sys


# # Classe liste simplement chaînée
# 
# ![Liste simplement chaînée](simplement_chainee.png)
# 
# 

# In[67]:


class Cellule:
    
    def __init__(self, info, suivant):
        self.info = info
        self.suivant = suivant    


class  ListeSimplementChainee:
    
    def __init__(self):
        self.premier = None
        self.taille = 0
    
    def est_vide(self):
        #return self.premier is None and self.dernier is None
        return self.premier is None
    
    
    def ajouterEnTete(self, e):        
        self.premier = Cellule(e, self.premier) 
        self.taille += 1

    def ajouterEnQueue(self, e):
        element = self.premier
        while element.suivant is not None:
            element = element.suivant
        element.suivant = Cellule(e, element.suivant) 
        self.taille += 1
        
    def supprimerTete(self):
        assert not self.est_vide()
        poubelle = self.premier
        self.premier = self.premier.suivant
        del poubelle
        self.taille -= 1
        
    
    def vider(self):
        while self.premier is not None:
            self.supprimerTete()
            self.taille -= 1
        
        
    def detruire(self):
        self.vider()
        del self.premier
        del self.taille
      
    
    def __str__(self):
        element = self.premier
        output = "["
        while element is not None:
            output += str(element.info) + ','
            element = element.suivant
        return output.rstrip(',') + ']'
    
    def afficher(self):
        print(str(self))
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        element1 = self.premier
        element2 = other.premier
        while element1 is not None and element2 is not None and element1.info == element2.info:
            element1 = element1.suivant
            element2 = element2.suivant            
        return element1 is None and element2 is  None

    def nb_elements(self):
        #return self.taille
        pointeur = self.premier
        compteur = 0
        while pointeur is not None:
            pointeur = pointeur.suivant
            compteur += 1
        return compteur
        
    def iemeElement(self, i):
        assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            return pointeur.info
        else:
            return None
        
    def modifierIemeElement(self, e, i):
        assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            pointeur.info = e
            
    
    def rechercherElement(self, e):
        pointeur = self.premier
        index = 0
        while pointeur is not None and pointeur.info != e:
            pointeur = pointeur.suivant
            index += 1
        return -1 if pointeur is None else index
    
    def insererElement(self, e, i):        
        n = self.nb_elements()
        assert 0 <= i <= n        
        if i == 0:
            self.premier = Cellule(e, self.premier)
        else:
            index = 0
            element = self.premier
            arret = i - 1
            while index != arret:
                element = element.suivant
                index += 1
            element.suivant = Cellule(e, element.suivant)
            self.taille += 1
        
        
    @staticmethod
    def simpleChainedList_from_Pythonlist(t):
        L = ListeSimplementChainee()
        for e in t:
            L.ajouterEnTete(e)
        return L
    
    def triInsertion(self):
        #complexité en O(n^2)
        #liste vide ou avec un élément => classée
        if self.est_vide() or self.premier.suivant is None: 
            return
        #liste avec au moins deux éléments
        precedent = self.premier
        element = self.premier.suivant        
        while element is not None:          
            #si la valeur de l'élément est inférieure à celle du premier élément classé
            val = element.info
            #print(val, self)
            #precedent.suivant = element.suivant
            prochainelement = element.suivant  
            precedent.suivant = prochainelement
            if val < self.premier.info: 
                element.suivant = self.premier
                self.premier  = element                              
            else:
                pretmp = self.premier
                tmp = self.premier.suivant
                #print(tmp.info, val)
                while tmp is not prochainelement and tmp.info < val:                    
                    pretmp = tmp
                    tmp = tmp.suivant 
                    #print(tmp.info)
                pretmp.suivant = element
                if tmp is  prochainelement:                    
                    precedent = element
                else:
                    element.suivant = tmp
            element = prochainelement      
            
    def triInsertion2(self):
        #liste vide ou avec un élément => classée
        if self.est_vide() or self.premier.suivant is None: 
            return
        n = self.taille
        if n <= 1: #liste de taille <= 1 => déjà triée
            return
        precedent = self.premier
        for i in range(1, n):
            element = precedent.suivant
            val = element.info
            #print(val, self)
            courant = self.premier
            j = 0
            while j < i and courant.info < val:
                courant = courant.suivant
                j = j + 1
            if j < i:
                poubelle = element                   
                precedent.suivant = element.suivant
                #complexité toujours en O(n^2) mais cette insertion nécessite un nouveau balayage depuis le début de la liste
                self.insererElement(val, j)  
                del poubelle
            else:
                precedent = precedent.suivant


# In[68]:


if __name__ == "__main__":
    L = ListeSimplementChainee()
    print(f"Attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")


    print("Ajout de list(range(6)) avec L.ajouterEnTete()")
    for k in range(6):
        L.ajouterEnTete(k)
    print("Affichage de la liste")
    L.afficher()
    n = L.nb_elements()
    print(f"Affichage du nombre d'éléments : {n}")
    for k in range(6):
        print(f" 0 <= k < L.nb_elements() : {0 <= k < n} et {k}-ieme élément : {L.iemeElement(k)}")
    print(f"Premier : {L.premier.info}  ")    

    print("-----------------------")


    print("On vide la liste")
    L.vider()
    print("Affichage de la liste")
    L.afficher()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")


    print("On détruit la liste")
    L.detruire()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")
    L = ListeSimplementChainee()
    print("Ajout de list(range(6)) avec L.ajouterEnQueue()")
    for k in range(6):
        L.ajouterEnTete(k)
    print("Affichage de la liste")
    L.afficher()
    print("Affichage de la liste")
    L.afficher()
    for k in range(6):
        print(f" 0 <= k < L.nb_elements() : {0 <= k < n}, on remplace le  {k}-ieme élément : {L.iemeElement(k)}"              f" par {k+1}  ")
        L.modifierIemeElement(k + 1, k)
    print("Affichage de la liste")
    L.afficher() 
    print(f"Premier : {L.premier.info}  ")

    print("-----------------------")
    print("Affichage de la liste")
    L.afficher() 
    print("Vidage de la liste avec supprimerTete")
    while L.premier is not None:
        L.supprimerTete()
    print("Affichage de la liste")
    L.afficher()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")
    print("Ajout de list(range(6)) avec L.ajouterEnTete()")
    for k in range(6):
        L.ajouterEnTete(k)
    print("Affichage de la liste")
    L.afficher()
    print(f"Insertion d'un élément en position {L.nb_elements() - 1},  dans la seconde moitié")
    L.insererElement(5.5, L.nb_elements() - 1)
    print("Affichage de la liste")
    L.afficher()
    print(f"Insertion d'un élément en position {1},  dans la première moitié")
    L.insererElement(0.5, 1)
    print("Affichage de la liste")
    L.afficher()
    print("----Test d'égalité---")
    L1 = ListeSimplementChainee.simpleChainedList_from_Pythonlist(range(10))
    L2 = ListeSimplementChainee.simpleChainedList_from_Pythonlist(range(10))
    print(f'L1={L1} et L2={L2} et L1 == L2 : {L1.__eq__(L2)}')


# In[69]:


# Test de triInsertion

from random import randint 
sample = [randint(1, 100) for _ in range(10)]
L = ListeSimplementChainee.simpleChainedList_from_Pythonlist(sample)
print(f"Avant tri L = {L}")
L.triInsertion()
print(ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)))
print(f"Après tri L = {L}, liste triée : {ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)) == L}")


# In[70]:


# Test de triInsertion2

from random import randint 
sample = [randint(1, 100) for _ in range(10)]
L = ListeSimplementChainee.simpleChainedList_from_Pythonlist(sample)
print(f"Avant tri L = {L}")
L.triInsertion2()
print(ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)))
print(f"Après tri L = {L}, liste triée : {ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)) == L}")


# # Classe liste doublement chaînée non circulaire
# 
# ![Liste doublement chainée non circulaire](doublement_chainee.png)
# 
# 
# Construire une classe implémentant les listes doublement chaînées non circulaires incluant :
# 
# * un constructeur et un destructeur
# * deux attributs premier et dernier qui sont des cellules
# * des méthodes estVide, vider, nbElements, iemeElement, modifierIemeElement, afficher, ajouterEnTete,
# ajouterEnQueue, supprimerTete, rechercherElement et insererElement
# 
# Vous définirez pour cela une classe-structure Cellule composée de trois attributs : info, suivant et precedent.
# 
# Écrire une procédure de la classe Liste qui, à partir d’un tableau d’éléments (liste Python), crée la liste chaînée contenant les mêmes éléments dans le même ordre. Donnez un exemple d’appel à cette procédure.
# 
# Écrivre une procédure de la classe Liste qui trie les éléments par ordre croissant, en utilisant l’algorithme du tri par insertion.
# 
# ![Fonctionnalités listes 1](fonctionnalites_listes.png)
# 
# 
# ![Fonctionnalités listes 2](fonctionnalites_listes2.png)

# In[71]:


class  Liste:
    
    def __init__(self):
        self.premier = None
        self.dernier = None
        self.taille = 0
    
    def est_vide(self):
        #return self.premier is None and self.dernier is None
        return self.premier is None
    
    def vider2(self):
        while self.premier is not None:
            poubelle = self.premier
            nouveau = self.premier.suivant
            if nouveau is not None:
                nouveau.precedent = self.premier
            self.premier = nouveau
            del poubelle
            self.taille -= 1
        self.dernier = self.premier
    
    def vider(self):
        while self.premier is not None:
            self.supprimerTete()
        self.dernier = self.premier
        
        
    def detruire(self):
        self.vider()
        del self.dernier
        del self.premier
        del self.taille
    
    def __del__(self):
        self.vider()
        del self.dernier
        del self.premier
        del self.taille
        
    def ajouterEnTete(self, e):
        nouveau = Cellule(e, None, self.premier)        
        if self.est_vide():  #si la liste est vide
            self.dernier = self.premier = nouveau
        else:
            self.premier.precedent = nouveau
            self.premier = nouveau 
        self.taille += 1


    def ajouterEnQueue(self, e):
        nouveau = Cellule(e, self.dernier, None)        
        if self.est_vide():  #si la liste est vide
            self.dernier = self.premier = nouveau
        else:
            self.dernier.suivant = nouveau
            self.dernier = nouveau 
        self.taille += 1
        
    def __str__(self):
        pointeur = self.premier
        output = "["
        while pointeur is not None:
            output += str(pointeur.info) + ','
            pointeur = pointeur.suivant
        return output.rstrip(',') + ']'   
    
    def afficher(self):
        print(str(self))   
         
    def nb_elements(self):
        #return self.taille
        pointeur = self.premier
        compteur = 0
        while pointeur is not None:
            pointeur = pointeur.suivant
            compteur += 1
        return compteur
        
    def iemeElement(self, i):
        assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            return pointeur.info
        else:
            return None
        
    def modifierIemeElement(self, e, i):
        assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            pointeur.info = e
            
            
    def supprimerTete(self):
        assert not self.est_vide()
        poubelle = self.premier
        nouveau = self.premier.suivant
        if nouveau is not None:
            nouveau.precedent = None
        self.premier = nouveau            
        if self.est_vide():
            self.dernier = self.premier
        del poubelle
        self.taille -= 1
    
    def rechercherElement(self, e):
        pointeur = self.premier
        index = 0
        while pointeur is not None and pointeur.info != e:
            pointeur = pointeur.suivant
            index += 1
        return -1 if pointeur is None else index
    
    def insererElement(self, e, i):        
        n = self.nb_elements()
        assert 0 <= i <= n       
        if i == 0:
            self.ajouterEnTete(e)
        elif i == n:
            self.ajouterEnQueue(e)
        elif i < n // 2:
            pointeur = self.premier
            index = 0
            while pointeur is not None and index != i:
                pointeur = pointeur.suivant
                index += 1
            avant = pointeur.precedent
            apres = pointeur
            nouveau = Cellule(e, avant, apres)
            avant.suivant = nouveau
            apres.precedent = nouveau
        else:
            pointeur = self.dernier
            index = n - 1
            while pointeur is not None and index != i:
                pointeur = pointeur.precedent
                index -= 1
            avant = pointeur.precedent
            apres = pointeur
            nouveau = Cellule(e, avant, apres)
            avant.suivant = nouveau
            apres.precedent = nouveau
        self.taille += 1
        
    @staticmethod
    def doubleChainedList_from_Pythonlist(t):
        L = Liste()
        for e in t:
            L.ajouterEnQueue(e)
        return L
    
    def triInsertion(self):
        #assert not self.est_vide()
        element = self.premier        
        while element is not None:
            avant = element.precedent
            val = element.info
            while avant is not None and avant.info > val:
                avant.suivant.info = avant.info
                avant = avant.precedent
            if avant is None:
                self.premier.info = val
            else:
                avant.suivant.info = val
            element = element.suivant
        
    
class Cellule:
    
    def __init__(self, info, precedent, suivant):
        self.info = info
        self.precedent = precedent
        self.suivant = suivant    
        
        


# In[72]:


if __name__ == "__main__":
    L = Liste()
    print(f"Attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")


    print("Ajout de list(range(6)) avec L.ajouterEnTete()")
    for k in range(6):
        L.ajouterEnTete(k)
    print("Affichage de la liste")
    L.afficher()
    n = L.nb_elements()
    print(f"Affichage du nombre d'éléments : {n}")
    for k in range(6):
        print(f" 0 <= k < L.nb_elements() : {0 <= k < n} et {k}-ieme élément : {L.iemeElement(k)}")
    print(f"Premier : {L.premier.info} et Dernier : {L.dernier.info} ")    

    print("-----------------------")


    print("On vide la liste")
    L.vider()
    print("Affichage de la liste")
    L.afficher()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")


    print("On détruit la liste")
    L.detruire()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")
    L = Liste()
    print("Ajout de list(range(6)) avec L.ajouterEnQueue()")
    for k in range(6):
        L.ajouterEnQueue(k)
    print("Affichage de la liste")
    L.afficher()
    print("Affichage de la liste")
    L.afficher()
    for k in range(6):
        print(f" 0 <= k < L.nb_elements() : {0 <= k < n}, on remplace le  {k}-ieme élément : {L.iemeElement(k)}"              f" par {k+1}  ")
        L.modifierIemeElement(k + 1, k)
    print("Affichage de la liste")
    L.afficher() 
    print(f"Premier : {L.premier.info} et Dernier : {L.dernier.info} ")

    print("-----------------------")
    print("Affichage de la liste")
    L.afficher() 
    print("Vidage de la liste avec supprimerTete")
    while L.premier is not None:
        L.supprimerTete()
    print("Affichage de la liste")
    L.afficher()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")
    print("Ajout de list(range(6)) avec L.ajouterEnTete()")
    for k in range(6):
        L.ajouterEnTete(k)
    print("Affichage de la liste")
    L.afficher()
    print(f"Insertion d'un élément en position {L.nb_elements() - 1},  dans la seconde moitié")
    L.insererElement(5.5, L.nb_elements() - 1)
    print("Affichage de la liste")
    L.afficher()
    print(f"Insertion d'un élément en position {1},  dans la première moitié")
    L.insererElement(0.5, 1)
    print("Affichage de la liste")
    L.afficher()


# ## Création d’une liste chaînée à partir d’un tableau
# 
# Écrire une procédure de la classe Liste qui, à partir d’un tableau d’éléments (liste Python), crée la liste chaînée contenant les mêmes éléments dans le même ordre. Donnez un exemple d’appel à cette procédure.

# In[73]:


L = Liste.doubleChainedList_from_Pythonlist([1,2,3])


# In[74]:


L.afficher()


# In[75]:


from random import randint


# In[76]:


L = Liste.doubleChainedList_from_Pythonlist([randint(1, 100) for _ in range(10)])
print("Avant tri ", L)
L.triInsertion()
print("Après tri ",L)


# In[77]:


#Test du tri par insertion sur les permutations de {0,1,2,3,4,5}

from itertools import permutations

collector = []
base = '[' + ','.join(map(str, list(range(6)))) + ']'
for p in permutations(range(6)):
    t = Liste.doubleChainedList_from_Pythonlist(list(p))
    t.triInsertion()
    collector.append(str(t) == base)
print(all(collector))

