#Listes doublement chainees non circulaire
from random import randint

class Cellule :
    def __init__(self, info, suivant=None, precedent=None) :
        self.info = info
        self.suivant = suivant
        self.precedent = precedent
        
class Liste :
    def __init__(self) :
        self.premier = None
        self.dernier = None
        
    def __str__(self):###repr ou str c'est pareil ???? nommer afficher ???
        ch = "Etat de la liste:\n"
        maillon = self.premier
        while maillon != None :
            ch +=  str(maillon.info) + " "
            maillon = maillon.suivant
        return ch
        
    def __len__(self):#renommer nbElements ???
        courant = self.premier
        cpt = 0
        while courant is not None:
            courant = courant.suivant
            cpt += 1
        return cpt
    
    def estVide(self):
        return len(self) == 0

    def ajout_en_tete(self, valeur):
        #Insère valeur en tête de liste en créant un nouveau maillon
        if len(self) == 0 :
            self.premier = self.dernier = Cellule(valeur)
        else :
            self.premier = Cellule(valeur,self.premier,self.dernier)
      
    def ajout_en_queue(self, valeur):
        if len(self) == 0 :
            self.ajout_en_tete(valeur)
        else :
            queue = Cellule(valeur)
            self.dernier.suivant = queue
            queue.precedent = self.dernier
            self.dernier = queue

    def supprimerEnTete(self) :
        #Supprime l'élément en tête et retourne ce dernier
        if len(self) == 0 :
            print("Liste vide !")
        else :
            tete = self.premier.info
            if len(self) > 1 :
                self.premier = self.premier.suivant
                self.dernier.precedent = self.premier
            else :
                self.premier = None
                self.dernier = None
            del tete

    def vider(self) :
        while self.premier :
            self.supprimerEnTete()

    def detruire(self) :
        #del self
        pass
        
    def iemeElement(self,i) :
        #affiche la ieme valeur de la liste, on commence à 1...
        assert(i<=len(self))
        courant = self.premier
        cpt = 0
        while cpt < i-1:
            courant = courant.suivant
            cpt += 1
        return(courant.info)
    
    def modifierIemeElement(self,i,valeur) :
        #remplace la valeur contenue à la position i dans la liste par valeur, on commence à 1...
        assert(i<=len(self))
        courant = self.premier
        cpt = 0
        while cpt < i-1:
            courant = courant.suivant
            cpt += 1        
        courant.info = valeur
        
    def rechercherElement(self,valeur) :
        #recherche si valeur est dans la liste, on peut rajouter compteur pour dire position...
        courant = self.premier
        while courant and courant.info != valeur :
            courant = courant.suivant      
        return courant != None and courant.info == valeur

    def insererElement(self,i,valeur) :
        #insert valeur à la ième position
        assert(1<i<len(self))
        courant = self.premier
        cpt = 0
        while cpt < i-2:
            courant = courant.suivant
            cpt += 1    
        apresInsert = courant.suivant
        courant.suivant = Cellule(valeur,apresInsert,courant)
        courant = courant.suivant
        apresInsert.precedent = courant

def listePythonDevientListeChainee(tab):
    #procedure qui à partir d'une liste python crée la liste chainée
    #faire procedure !!!!!
    lCh = Liste()
    for val in tab :
        lCh.ajout_en_queue(val)
    return lCh

def triInsertionListeCh(lCh):
    #procedure ????  
    '''La fonction prend en argument une liste chainée d'éléments comparables et renvoie 
       la liste chainée composée des mêmes éléments, triés par insertion dans l'ordre croissant'''
    for i in range (1,len(lCh)) :   #place L[i] parmi les i-1 premiers termes triés
        carte = lCh.iemeElement(i+1)
        position = i            
        while position >= 1 and carte < lCh.iemeElement(position) :
            lCh.modifierIemeElement(position+1,lCh.iemeElement(position)) #pousse L[i] à droite tant que nécessaire
            position -=1
        lCh.modifierIemeElement(position+1,carte)           #insère finalement L[i] à sa place
    return L
   

        
L = Liste()
L.supprimerEnTete() 
L.ajout_en_tete(3)
print(L)
L.supprimerEnTete()       
print(L)
L.ajout_en_tete(4)
L.ajout_en_tete(1)
print(L)
L.ajout_en_queue(7)
L.ajout_en_queue(8)
L.ajout_en_queue(17)
print(L)
print("La file est-elle vide: ", L.estVide())
print("Longueur de la file: ", len(L))
L.supprimerEnTete()       
print(L)
L.vider()
print(L)

L = Liste()
L.ajout_en_tete(4)
L.ajout_en_tete(3)
L.ajout_en_tete(1)
L.ajout_en_queue(7)
L.ajout_en_queue(8)
L.ajout_en_queue(17)
print(L.iemeElement(2))
print(L)
L.modifierIemeElement(2,100)
print(L)
print(L.rechercherElement(7))
print(L.rechercherElement(77))
L.insererElement(4,80)
print(L)


listePython = [randint(0,100) for i in range(20)]
print(listePython)
listeCh = listePythonDevientListeChainee(listePython)
print(listeCh)
print(type(listeCh))
triInsertionListeCh(listeCh)
print(listeCh)