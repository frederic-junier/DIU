
# coding: utf-8

# In[162]:


import sys


# # Classe liste simplement chaînée circulaire
# 
# 
# ![Liste simplement chainée](ListeSimplementChaineeCirculaire.png)

# In[163]:


class Cellule:
    
    def __init__(self, info, suivant):
        self.info = info
        self.suivant = suivant    


class  ListeSimplementChaineeCirculaire:
    
    def __init__(self):
        self.premier = None
        #on rajoute un accès au dernier élément pour faciliter l'ajout en tete
        self.dernier = None  
        self.taille = 0
    
    def est_vide(self):
        #return self.premier is None and self.dernier is None
        return self.premier is None
    
    def __len__(self):
        #return self.taille
        if self.est_vide():
            return 0
        n = 1
        debut = self.premier
        pointeur = self.premier
        while pointeur.suivant is not debut:
            pointeur = pointeur.suivant
            n += 1
        return n
    
    def nbElements(self):
        return len(self)
    
    
    def ajouterEnTete(self, e):   
        elt =  Cellule(e, self.premier)        
        if self.est_vide():               
            elt.suivant = elt
            self.dernier = elt
        self.premier = elt
        self.dernier.suivant = self.premier
        self.taille += 1

    def ajouterEnQueue(self, e):
        if self.est_vide():
            self.ajouterEnTete(e)
        else:
            self.dernier.suivant = Cellule(e, self.premier)
            self.dernier = self.dernier.suivant
        self.taille += 1
        
    def supprimerTete(self):
        assert not self.est_vide(), "liste vide !"
        poubelle = self.premier 
        #cas particulier : liste réduite à un élément 
        #car  premier = dernier et premier.suivant = premier
        if len(self) == 1:
            #self.premier = self.dernier = self.dernier.suivant = None  => non
            self.dernier.suivant = None
            self.premier = None
            self.dernier = None
        else:
            self.premier = self.premier.suivant
            self.dernier.suivant = self.premier
        self.taille -= 1
        del poubelle
       
    
    def vider(self):
        while not self.est_vide():
            self.supprimerTete()
        
    def __del__(self):
        print(f"Destruction de {repr(self)}")        
      
    
    def __str__(self):
        if self.est_vide():
            return '[]'
        debut = self.premier
        output = "[" + str(debut.info) + ','
        element = debut.suivant
        while element is not debut:
            output += str(element.info) + ','
            element = element.suivant
        return output.rstrip(',') + ']'
      
    def afficher(self):
        print(self)
    
    def __eq__(self, other):
        assert isinstance(other, type(self)), "éléments de types différents"
        debut1 = self.premier
        debut2 = other.premier
        pointeur1 = self.premier
        pointeur2 = other.premier
        while pointeur1 is not None and pointeur2 is not None               and pointeur1.info == pointeur2.info and pointeur1.suivant is not debut1               and pointeur2.suivant is not debut2:
            pointeur1 = pointeur1.suivant
            pointeur2 = pointeur2.suivant
        #listes égales ssi elles sont vides ou si elles sont de même taille avec toutes les valeurs égales
        return pointeur1 is None and pointeur2 is None or pointeur1.info == pointeur2.info                 and pointeur1.suivant is debut1  and pointeur2.suivant is  debut2
        
       
        
    def iemeElement(self, i):
        assert not self.est_vide(), "liste vide !"
        assert i >= 0, "i négatif"
        n = len(self)
        i = i % n      
        pointeur = self.premier
        index = 0
        while index < i:
            pointeur = pointeur.suivant
            index += 1
        return pointeur.info
        
    def modifierIemeElement(self, i, e):
        assert i >= 0 and  not self.est_vide(), "liste vide !"
        pointeur = self.premier
        index = 0
        while index < i:
            pointeur = pointeur.suivant
            index += 1
        pointeur.info = e
            
    
    def rechercherElement(self, e):
        """Retourne la position de l'élément ou -1 s'il n'est pas dans """
        assert not self.est_vide(), "liste vide !"
        debut = self.premier
        pointeur = self.premier
        index = 0
        while pointeur.info != e and pointeur.suivant is not debut:
            pointeur = pointeur.suivant
            index += 1
        if pointeur.info == e:
            return index
        return -1
    
    def insererElement(self, i, e):
        if self.est_vide():
            self.ajouterEnTete(e)
        n = len(self)
        i = i % n
        precedent = self.premier
        pointeur = self.premier.suivant
        index = 1
        while index != i:
            precedent = precedent.suivant
            pointeur = pointeur.suivant
            index += 1
        precedent.suivant = Cellule(e, pointeur)
        self.taille += 1
    
    def importerTableau(self, tab):
        for e in tab:
            self.ajouterEnTete(e)
            
    def permutationCirculaireDirecte(self):
        self.dernier, self.premier = self.premier, self.premier.suivant 


# In[164]:


lcc = ListeSimplementChaineeCirculaire()
lcc.importerTableau([1,2])
print(lcc.premier.suivant.suivant.suivant.info)
print(lcc)
lcc.supprimerTete()
print(lcc)


# In[165]:


lc = ListeSimplementChaineeCirculaire()
print("Ajout en tete de 5 '2' 4 : ", end='')
lc.ajouterEnTete(5)
lc.ajouterEnTete("2")
lc.ajouterEnTete(4)
lc.afficher()

print("Valeur de l'element a l'indice 1 : ", lc.iemeElement(1))

print("Modification de l'element a l'indice 1 (1.6) : ", end='')
lc.modifierIemeElement(1, 1.6)
lc.afficher()

print("Nombre d'elements : ", lc.nbElements())

print("Suppression de l'element de tete : ", end='')
lc.supprimerTete()
lc.afficher()

print("Ajout en queue de 7 et 'test' : ", end='')
lc.ajouterEnQueue(7)
lc.ajouterEnQueue("test")
lc.afficher()

print("Recherche de la valeur 5 : ", lc.rechercherElement(5))
print("Recherche de la valeur 'coucou' : ", lc.rechercherElement("coucou"))

print("Insertion de la valeur 10 a l'indice 3 : ", end='')
lc.insererElement(3, 10)
lc.afficher()

print("Après suppression de tous les elements : ", end='')
lc.vider()
lc.afficher()

tab = [5,4,'a',-1]
print("Ajout en tete de 5, 4, 'a' et -1 : ", end='')
lc.importerTableau(tab)
lc.afficher()

lc.vider()
lc.ajouterEnTete(5)
lc.ajouterEnTete(2)
lc.ajouterEnTete(4)
lc.ajouterEnTete(-1)
lc.ajouterEnTete(0)
lc.ajouterEnTete(8)
print("Liste : ", end='')
lc.afficher()
lc.vider()

tab = [5,4,'a',-1]
print("Ajout en tete de 5, 4, 'a' et -1 : ", end='')
lc.importerTableau(tab)
lc.afficher()


print("Création d'une liste lc2 avec les mêmes éléments")
lc2 = ListeSimplementChaineeCirculaire()
lc2.importerTableau(tab)
lc2.afficher()
print("lc == lc2")
print(lc.__eq__(lc2))
print("Modification du second élément de lc2")
lc2.modifierIemeElement(1, 7)
print("lc == lc2")
print(lc.__eq__(lc2))


print('Permutation circulaire directe')
lc.afficher()
for k in range(len(lc)):
    lc.permutationCirculaireDirecte()
    lc.afficher()
    


# # Classe liste simplement chaînée non circulaire
# 
# ![Liste simplement chaînée](simplement_chainee.png)
# 
# 

# In[166]:


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


# In[167]:


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


# In[168]:


# Test de triInsertion

from random import randint 
sample = [randint(1, 100) for _ in range(10)]
L = ListeSimplementChainee.simpleChainedList_from_Pythonlist(sample)
print(f"Avant tri L = {L}")
L.triInsertion()
print(ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)))
print(f"Après tri L = {L}, liste triée : {ListeSimplementChainee.simpleChainedList_from_Pythonlist(sorted(sample, reverse = True)) == L}")


# In[169]:


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

# In[170]:


class Cellule:
    
    def __init__(self, info, precedent, suivant):
        self.info = info
        self.precedent = precedent
        self.suivant = suivant    


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
            #print(self.premier.info)
            self.supprimerTete()
            self.taille -= 1
        #self.dernier = self.premier  => non géré par supprimerTete
        
        
    def detruire(self):
        self.vider()
        #rint(vars(self))
        #les lignes suivantes posent problème
        #del self.dernier
        #del self.premier
        #del self.taille
    
    def __del__(self):
        print(f"La liste d'identifiant {id(self)} va être détruite")
        #self.vider()
        #del self.dernier
        #del self.premier
        #del self.taille
        
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
    
    
    def ajouterEnQueue2(self, e):
        nouveau = Cellule(e, self.dernier, None)        
        if self.est_vide():  #si la liste est vide
            self.ajouterEnTete(e)
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
        #assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            return pointeur.info
        else:
            return None
        
    def iemeElement2(self, i):
        assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while  index != i:
            index += 1
            pointeur = pointeur.suivant
        return pointeur.info

        
    def modifierIemeElement(self, e, i):
        #assert 0 <= i < self.nb_elements()
        index = 0
        pointeur = self.premier
        while pointeur is not None and index != i:
            index += 1
            pointeur = pointeur.suivant
        if pointeur is not None:
            pointeur.info = e
    
    def modifierIemeElement2(self, e, i):
        index = 0
        pointeur = self.premier
        while  index != i:
            index += 1
            pointeur = pointeur.suivant
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
    
    def insererElement2(self, e, i): 
        n = self.nb_elements()
        assert 0 <= i <= n
        if i == 0:
            self.ajouterEnTete(e)
        elif i == n:
            self.ajouterEnQueue(e)
        else:
            pointeur = self.premier
            index = 0
            while  index != i:
                pointeur = pointeur.suivant
                index += 1
            avant = pointeur.precedent 
            avant.suivant = Cellule(e, avant, pointeur)
            pointeur.precedent = avant.suivant
            
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
            #print(index, i)
            while pointeur is not None and index != i:
                pointeur = pointeur.precedent
                print(pointeur.info)
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
    
    @staticmethod
    def doubleChainedList_from_Pythonlist2(listechainee, listepython):
        assert listechainee.est_vide()
        for e in  listepython:
            listechainee.ajouterEnQueue(e) 
    
    
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
        
    

        
        


# In[171]:


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

    print("Affichage de la liste")
    L.afficher()
    print("On vide la liste")
    L.vider()
    print("Affichage de la liste")
    L.afficher()
    print(f"attributs : {vars(L)}, identifiants : {id(L)} et taille en octets : {sys.getsizeof(L)}")


    print("-----------------------")


    print("On détruit la liste")
    del(L)
   


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
    print(f"attributs : {vars(L)}, identifiants : {id(L)} ")


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


# In[172]:


L = Liste()
print("Ajout de list(range(6)) avec L.ajouterEnTete()")
for k in range(3):
    L.ajouterEnTete(k)
print("Affichage de la liste")
L.afficher()
print(L.nb_elements() - 1)
L.insererElement(5.5, L.nb_elements() - 1)
L.afficher()
"""
L.afficher()
L.supprimerTete()
L.afficher()
L.supprimerTete()
L.afficher()
L.supprimerTete()
L.afficher()
L.supprimerTete()
L.afficher()
"""
L.vider()
L.afficher()


# ## Création d’une liste chaînée à partir d’un tableau
# 
# Écrire une procédure de la classe Liste qui, à partir d’un tableau d’éléments (liste Python), crée la liste chaînée contenant les mêmes éléments dans le même ordre. Donnez un exemple d’appel à cette procédure.

# In[173]:


L = Liste.doubleChainedList_from_Pythonlist([1,2,3])


# In[174]:


L.afficher()


# In[175]:


from random import randint


# In[176]:


L = Liste.doubleChainedList_from_Pythonlist([randint(1, 100) for _ in range(10)])
print("Avant tri ", L)
L.triInsertion()
print("Après tri ",L)


# In[177]:


#Test du tri par insertion sur les permutations de {0,1,2,3,4,5}

from itertools import permutations

collector = []
base = '[' + ','.join(map(str, list(range(6)))) + ']'
for p in permutations(range(6)):
    t = Liste.doubleChainedList_from_Pythonlist(list(p))
    t.triInsertion()
    collector.append(str(t) == base)
print(all(collector))


# # Classe liste doublement chaînée circulaire
# 
# ![liste doublement chaînée](liste_doublement_chainee_circulaire.png)

# In[182]:


class Cellule:
    
    def __init__(self, info, precedent= None, suivant = None):
        self.info = info
        self.precedent = precedent
        self.suivant = suivant    


class  ListeDoublementChaineeCirculaire:
    
    def __init__(self):
        self.premier = None
        self.dernier = None
        self.taille = 0
        
    def est_vide(self):
        return self.premier is None
    
    def __len__(self):
        #return self.taille
        if self.est_vide():
            return 0
        n = 1
        debut = self.premier
        suivant = debut.suivant
        while suivant is not debut:
            n += 1
            suivant = suivant.suivant
        return n
    
    def nbElements(self):
        return len(self)
        
    
    
    def supprimerTete(self):
        assert not self.est_vide(), "liste vide !"
        poubelle = self.premier
        #si la liste n'est pas réduite à un élément
        #on détache le premier et on met à jour les liens
        if self.premier.suivant is not self.premier:
            self.premier = self.premier.suivant  #lien d'accès au premier
            self.premier.precedent = self.dernier  #lien du premier vers le dernier
            self.dernier.suivant = self.premier    #lien du dernier vers le premier
        #sinon on revient à une liste vide
        else:
            self.premier = self.dernier = None
        #on a supprimé tous les liens vers poubelle
        #on détruit poubelle
        del poubelle
        #on met à jour la taille
        self.taille -= 1
        
    def supprimerQueue(self):
        assert not self.est_vide(), "liste vide !"
        poubelle = self.dernier
        #si la liste n'est pas réduite à un élément
        #on détache le dernier et on met à jour les liens
        if self.dernier.precedent is not self.dernier:
            self.dernier = self.dernier.precedent #lien d'accès au drnir
            self.premier.precedent = self.dernier  #lien du premier vers le dernier
            self.dernier.suivant = self.premier    #lien du dernier vers le premier
        #sinon on revient à une liste vide
        else:
            self.premier = self.dernier = None
        #on a supprimé tous les liens vers poubelle
        #on détruit poubelle
        del poubelle
        #on met à jour la taille
        self.taille -= 1
        
            
    def vider(self):
        while self.premier is not None:
            self.supprimerTete()
            
    def __del__(self):
        #print(f"La liste d'identifiant {id(self)} va être détruite")
        pass
        
        
    def ajouterEnTete(self, e):
        elt = Cellule(e, self.dernier, self.premier)
        if self.est_vide():
            self.premier = elt
            self.dernier = self.premier
            self.premier.precedent =  elt
            self.premier.suivant =  elt
        else:
            self.premier.precedent = elt
            self.premier = elt
            self.dernier.suivant = self.premier
        self.taille += 1
        
    def ajouterEnQueue(self, e):        
        if self.est_vide():
            self.ajouterEnTete(e)
        else:
            elt = Cellule(e, self.dernier, self.premier)
            self.dernier.suivant = elt
            self.dernier = elt
            self.premier.precedent = self.dernier
        self.taille += 1
        
        
    def __str__(self):
        if self.est_vide():
            return '[]'        
        debut = self.premier
        output = '[' + str(debut.info)
        suivant = debut.suivant
        while suivant is not debut:
            output += ',' + str(suivant.info)
            suivant = suivant.suivant
        return output + ']'
    
    def afficher(self):
        print(str(self))   
       
        
        
    def iemeElement(self, i):
        n = self.nbElements()
        assert 0 <= i 
        i = i % n        
        index = 0
        element = self.premier
        while index < i:
            element= element.suivant
            index += 1
        return element.info

        
    def modifierIemeElement(self, i, e):
        n = len(self)
        assert 0 <= i 
        i = i % n        
        index = 0
        element = self.premier
        while index < i:
            element= element.suivant
            index += 1
        element.info = e
  
       
    def rechercherElement(self, e):
        assert not self.est_vide(), "Liste vide !"
        debut = self.premier
        element = self.premier
        index = 0
        while element.info != e and element.suivant is not debut:
            element = element.suivant
            index += 1
        if element.info == e:
            return index
        return -1
            
    def insererElement(self, e, i):        
        if self.est_vide():
            self.ajouterEnTete(e)
        n = len(self)
        i = i % n
        if i == 0:
            self.ajouterEnQueue(e)
        element = self.premier
        index = 0
        while index < i:
            element = element.suivant
            index += 1
        elt = Cellule(e, element.precedent, element)
        element.precedent.suivant = elt
        element.precedent = elt
        self.taille += 1
    
    def __eq__(self, other):
        assert isinstance(other, type(self)), "objets de types différents"
        debut1  = self.premier
        debut2 = other.premier
        element1 = self.premier
        element2 = other.premier
        while element1 is not None and element2 is not None              and element1.suivant is not debut1 and element2.suivant is not debut2             and element1.info == element2.info:
                element1 = element1.suivant
                element2 = element2.suivant
        return (element1 is None and element2 is None                 or (element1.info == element2.info                     and element1.suivant is debut1                     and element2.suivant is debut2 ))
        
        
    def importerTableau(self, tab):
        for e in tab:
            self.ajouterEnQueue(e)
    
    def permutationCirculaireDirecte(self):
        self.dernier, self.premier = self.premier, self.premier.suivant
        
    def permutationCirculaireIndirecte(self):
        self.dernier, self.premier = self.dernier.precedent, self.dernier
        
    def triInsertion(self):
        debut = self.premier
        aPlacer = self.premier.suivant
        #boucle sur les éléments non classés
        while aPlacer is not debut:
            dernierTri = aPlacer.precedent
            courant = self.premier
            val = aPlacer.info
            #boucle interne sur les éléments classés
            #pour déterminer le point d'insertion
            while courant is not aPlacer and courant.info < val:                
                courant = courant.suivant
                #print("Courant", courant.info)
            #3 cas d'insertion
            #il faut déplacer aPlacer
            if courant is not aPlacer:
                #mise à jour des liens entre dernierTri et aPlacer.suivant
                dernierTri.suivant = aPlacer.suivant
                aPlacer.suivant.precedent = dernierTri
                #attention sous-cas : 
                #si aPlacer est le dernier élément
                #mettre à jour self.dernier car on déplace aPlacer
                if aPlacer is self.dernier:
                    self.dernier = dernierTri
                #insertion en tête de liste
                if courant is self.premier: 
                    #on change les liens partant de aPlacer                    
                    aPlacer.precedent = self.dernier
                    aPlacer.suivant = self.premier
                    #on change le lien partant de aPlacer
                    self.premier.precedent = aPlacer                
                    self.premier = aPlacer
                    self.dernier.suivant = self.premier
                #insertion entre la tête de liste et dernierTri
                else:
                    #on a 4 liens à changer
                    aPlacer.precedent = courant.precedent
                    aPlacer.suivant = courant
                    courant.precedent = aPlacer                
                    aPlacer.precedent.suivant = aPlacer    
            #cas où on ne déplace pas aPlacer qui devient dernierTri
            else: 
                dernierTri = aPlacer
            #print(self)
            aPlacer = dernierTri.suivant            


# In[179]:


lc = ListeDoublementChaineeCirculaire()
print("Ajout en tete de 5 '2' 4 : ", end='')
lc.ajouterEnTete(5)
lc.ajouterEnTete("2")
lc.ajouterEnTete(4)
lc.afficher()

print("Valeur de l'element a l'indice 1 : ", lc.iemeElement(1))

print("Modification de l'element a l'indice 1 (1.6) : ", end='')
lc.modifierIemeElement(1, 1.6)
lc.afficher()

print("Nombre d'elements : ", lc.nbElements())

print("Suppression de l'element de tete : ", end='')
lc.supprimerTete()
lc.afficher()

print("Ajout en queue de 7 et 'test' : ", end='')
lc.ajouterEnQueue(7)
lc.ajouterEnQueue("test")
lc.afficher()

print("Recherche de la valeur 5 : ", lc.rechercherElement(5))
print("Recherche de la valeur 'coucou' : ", lc.rechercherElement("coucou"))

print("Insertion de la valeur 10 a l'indice 3 : ", end='')
lc.insererElement(3, 10)
lc.afficher()

print("Après suppression de tous les elements : ", end='')
lc.vider()
lc.afficher()

tab = [5,4,'a',-1]
print("Ajout en tete de 5, 4, 'a' et -1 : ", end='')
lc.importerTableau(tab)
lc.afficher()

lc.vider()
lc.ajouterEnTete(5)
lc.ajouterEnTete(2)
lc.ajouterEnTete(4)
lc.ajouterEnTete(-1)
lc.ajouterEnTete(0)
lc.ajouterEnTete(8)
print("Liste : ", end='')
lc.afficher()
lc.vider()

tab = [5,4,'a',-1]
print("Ajout en tete de 5, 4, 'a' et -1 : ", end='')
lc.importerTableau(tab)
lc.afficher()


print("Création d'une liste lc2 avec les mêmes éléments")
lc2 = ListeDoublementChaineeCirculaire()
lc2.importerTableau(tab)
lc2.afficher()
print("lc == lc2")
print(lc.__eq__(lc2))
print("Modification du second élément de lc2")
lc2.modifierIemeElement(1, 7)
print("lc == lc2")
print(lc.__eq__(lc2))
print("On remet le même second élément mais on rallonge lc2")
lc2.modifierIemeElement(1, lc.iemeElement(1))
lc2.ajouterEnQueue(lc.iemeElement(1))
print("lc == lc2")
print(lc.__eq__(lc2))


print('Permutation circulaire directe')
lc.afficher()
for k in range(len(lc)):
    lc.permutationCirculaireDirecte()
    lc.afficher()
    
print('Permutation circulaire indirecte')
lc.afficher()
for k in range(len(lc)):
    lc.permutationCirculaireIndirecte()
    lc.afficher()


# In[180]:


#Un exemple de tri 
L = ListeDoublementChaineeCirculaire()
L.importerTableau(list(range(6, -1, -1)))
print('Avant tri')
L.afficher()
print('Après tri')
L.triInsertion()
L.afficher()


# In[181]:


# Test de triInsertion
from itertools import permutations

collector = []
base = '[' + ','.join(map(str, list(range(6)))) + ']'
for p in permutations(range(6)):
    L = ListeDoublementChaineeCirculaire()
    L.importerTableau(list(p))
    L.triInsertion()
    collector.append(str(L) == base)
print(all(collector))

