class Cellule:
    """ Type de base pour les noeuds de la file """

    def __init__(self, info_element, suivant):
        self.info = info_element
        self.suivant = suivant


class File:
    """ File du type FIFO à l'aide d'une liste chainée simple """
    
    def __init__(self):
        self.tete = None    # Attention dans l'ordre de chainage la tête est à gauche et la queue à droite
        self.queue = None   # On defile en tete (à gauche) et on enfile en queue (à droite)
        
    def est_vide(self):
        """" Renvoie True si et seulement si la file est vide"""
        
        return self.tete is None


    def afficher(self):
        """" Affiche tous les éléments de la file avec print(). Ne renvoie rien."""

        cel = self.tete
        while cel is not None:
            print(cel.info, end = ' ')
            cel = cel.suivant


    def enfiler(self, info_element):
        """"Ajoute un élément dans la file. Ne renvoie rien."""

        if self.est_vide():
            cel = Cellule(info_element, None)
            self.tete = cel
            self.queue = cel
        else:
            cel = Cellule(info_element, None)
            self.queue.suivant = cel
            self.queue = cel
            

    def defiler(self):
        """ renvoie le dernier élément de la file et le retire de la file """
        
        assert not self.est_vide(), 'La file est vide'
        info = self.tete.info
        if self.tete is self.queue:
            del self.tete
            self.tete = None
            self.queue = None
        else:
            tete = self.tete
            self.tete = tete.suivant
            del tete
        return info

# =========================  Arbre (non ABR) ===========================
            
class Arbre:

    def __init__(self, info = None, fg = None, fd = None):
        """ Postconditions : l'arbre est vide """
        self.info = info
        self.fg = fg
        self.fd = fd

    def __del__(self):
        pass

    def vider(self):
        pass

    def est_vide(self):
        """ Teste si l'arbre est vide """
        return self.info is None

    def afficher(self):
        pass
    
    
    def afficherParcoursInfixe(self):
        if self.info is not None:
            if self.fg is not None:
                self.fg.afficherParcoursInfixe()
            print(self.info, end =' ')
            if self.fd is not None:
                self.fd.afficherParcoursInfixe()

    def afficherParcoursPrefixe(self):
        if self.info is not None:
            print(self.info, end =' ')
            if self.fg is not None:
                self.fg.afficherParcoursPrefixe()
            if self.fd is not None:
                self.fd.afficherParcoursPrefixe()

    def afficherParcoursPostfixe(self):
        if self.info is not None:
            if self.fg is not None:
                self.fg.afficherParcoursPostfixe()
            if self.fd is not None:
                self.fd.afficherParcoursPostfixe()
            print(self.info, end =' ')

    def afficherParcoursLargeur(self):
        f = File()
        if self.info is not None:
            f.enfiler(self)
        while not f.est_vide():
            noeud = f.defiler()
            if noeud.fg:f.enfiler(noeud.fg)
            if noeud.fd:f.enfiler(noeud.fd)
            print(noeud.info, end = ' ')


    def hauteurArbre(self):
        h = -1
        f = File()
        if self.info is not None:
            f.enfiler((self, 0))   # On place le noeud avec sa profondeur dans la file
        while not f.est_vide():
            (noeud, prof) = f.defiler()
            if prof > h:
                h = prof
            if noeud.fg:f.enfiler((noeud.fg, prof + 1))
            if noeud.fd:f.enfiler((noeud.fd, prof + 1))
        return h
        
    def afficherParcoursPrefixe_iter(self):

        if self.info is not None:
            pile = [self]           # On utilise une liste python comme pile
        while len(pile) > 0:
            a = pile.pop()
            print(a.info, end =' ')
            if a.fd is not None:
                pile.append(a.fd)
            if a.fg is not None:
                pile.append(a.fg)

    def est_egal(self, arbre):
        print(self.info, arbre.info)
        if self.info is None or arbre.info is None: # Cas où l'un des arbres est vide
            return self.info == arbre.info
        # Ici aucun des arbres n'est vide
        if (self.fg and not arbre.fg) or (not self.fg and arbre.fg):
            return False    # Cas où il y a un fg sur l'un des arbres mais pas sur l'autre
        if (self.fd and not arbre.fd) or (not self.fd and arbre.fd):
            return False    # Cas où il y a un fd sur l'un des arbres mais pas sur l'autre
        egal_a_gauche = (self.fg is None and arbre.fg is None) or self.fg.est_egal(arbre.fg)
        egal_a_droite = (self.fd is None and arbre.fd is None) or self.fd.est_egal(arbre.fd)
        return egal_a_gauche and egal_a_droite

    
    def rechercherElement(self, elt):

        if self.info is None:
            return (False, None)
        else:
            pile = [self]           # On utilise une liste python comme pile
        while len(pile) > 0:
            a = pile.pop()
            if a.info == elt:
                return (True, a)
            if a.fd is not None:
                pile.append(a.fd)
            if a.fg is not None:
                pile.append(a.fg)
        return (False, None)
        

    def est_ABR(self, mini = float('-inf'), maxi = float('+inf')):
        """ Teste si self est un ABR dont les noeuds sont strictement compris
        entre mini et maxi"""

#        print(self.info, mini, maxi)
        if self.info is None:
            return True
        if not mini < self.info < maxi:
            return False
        gauche = (self.fg == None) or self.fg.est_ABR(mini, self.info)
        droite = (self.fd == None) or self.fd.est_ABR(self.info, maxi)
        return gauche and droite

    def somme_maxi_glouton(self):
        S = 0
        arbre = self
        while arbre.info is not None:
            S += arbre.info
            if arbre.fg is None and arbre.fd is None:
                break
            gauche = float('-inf') if arbre.fg is None else arbre.fg.info
            droite = float('-inf') if arbre.fd is None else arbre.fd.info
            if gauche > droite:   
                arbre = arbre.fg
            else:
                arbre = arbre.fd
        return S
                
# Si l'arbre comporte une grande valeur derrière une petite l'algo va la rater,
# dans un cas de ce type l'algo ne donnera pas la valeur optimale. 
# Complexité dans le pie des cas = hauteur de l'arbre
 
            
    def somme_maxi_dyn(self):
        if self.info is None:
            return 0
        S = self.info
        gauche = self.fg.somme_maxi_dyn() if self.fg else 0
        droite = self.fd.somme_maxi_dyn() if self.fd else 0
        return S + max(gauche, droite)
    
# Complexité = O(S) où S = nb de sommets
    

# =========================  ARBRE BINAIRE DE RECHERCHE ===========================

class ABR(Arbre):

    def insererElement(self, elt):
        if self.info is None:
            self.info = elt
        elif self.info < elt:
            if self.fd is None:
                self.fd = ABR(elt)
            else:
                self.fd.insererElement(elt)
        elif elt < self.info:
            if self.fg is None:
                self.fg = ABR(elt)
            else:
                self.fg.insererElement(elt)
        
    def rechercherElement(self, elt):
        if self.info is None:
            return (False, None)
        elif self.info < elt:
            if self.fd is None:
                return (False, None)
            else:
                return self.fd.rechercherElement(elt)
        elif elt < self.info:
            if self.fg is None:
                return (False, None)
            else:
                return self.fg.rechercherElement(elt)
        else:
            return (True, self)
        

        
        
# ===============  Pour les tests  ================


A0 = Arbre()  # A0 et un arbre vide

A1 = Arbre(1) # A1 est un arbre qui ne comporte qu'un seul noeud dont l'info est l'entier 1

A2 = Arbre(2)       #   A2:     2
A2.fg = Arbre(1)    #         /   \
A2.fd = Arbre(3)    #        1     3    A2 est un ABR

A3 = Arbre(6)

B = ABR(5)
B.insererElement(2)
B.insererElement(1)
B.insererElement(7)
B.insererElement(6)
B.insererElement(9)

A = ABR(5)
A.insererElement(2)
A.insererElement(1)
A.insererElement(7)
A.insererElement(6)
A.insererElement(9)

C = ABR(5)
C.insererElement(2)
C.insererElement(1)
C.insererElement(9)
C.insererElement(6)
C.insererElement(7)







    
            

        
