from PileFile import File, Pile
from random import randint

class Arbre :
    # ArbreBinaireDeRecherche
    def __init__(self, info=None, fg=None, fd=None, val = 0) :
        self.info = info
        self.fg = fg
        self.fd = fd
        
    def estVide(self) :
        return self.info is None
        
    def insererElement(self, elmt) :
        if not self.info :    # le sous arbre est vide, on est arrivé au bon endroit pour insérer
            self.info = elmt
        else :
            if elmt < self.info :
                if self.fg :  #le sous arbre existe déjà, on continue
                    self.fg.insererElement(elmt)
                else :        # le sous arbre n'existe pas, on le crée
                    self.fg= Arbre(elmt)
            if elmt > self.info :
                if self.fd :
                    self.fd.insererElement(elmt)
                else:
                    self.fd= Arbre(elmt)
            # rien à faire si égal, déjà présent, arrêt de la récursion

    #proposition de Pascal Salliot
    def affichage(self, niveau=0, c=132):
        if self.fd:
            self.fd.affichage( niveau+1, 47 )
        print(f"{4 * niveau * ' '}{chr(c)}{self.info}")
        if self.fg:
            self.fg.affichage( niveau+1, 92 )

    def afficherParcoursInfixe(self) :
        if self.info :
            if self.fg :                                
                self.fg.afficherParcoursInfixe()
            print(self.info, end=' ') # on traite le noeud
            if self.fd :
                self.fd.afficherParcoursInfixe()

#     def afficherParcoursInfixe_iter(self) :
#         p = Pile([])
#         other = self
#         while other or not p.estVide() :
#             while other :
#                 if other.fg :
#                     p.empiler(other.fg)
#                 other = other.fg
#             p.traiter()

    def afficherParcoursPrefixe(self) :
        if self.info :
            print(self.info, end=' ') # on traite le noeud
            if self.fg :
                self.fg.afficherParcoursPrefixe()
            if self.fd :
                self.fd.afficherParcoursPrefixe()

    def afficherParcoursPrefixeIteratif(self) :
        if self.info :
            p = Pile([])
            p.empiler(self)
            while not p.estVide() :
                n = p.traiter()
                print(n.info, end=' ')      # on traite le noeud
                if n.fd :
                    p.empiler(n.fd)
                if n.fg :
                    p.empiler(n.fg)

    def afficherParcoursPostfixe(self) :
        if self.info :
            if self.fg :
                self.fg.afficherParcoursPostfixe()
            if self.fd :
                self.fd.afficherParcoursPostfixe()
            print(self.info, end=' ') # on traite le noeud
            
    def afficherParcoursLargeur(self) :
        f = File([])
        f.enfiler(self)
        while not f.estVide() :
            n = f.traiter()
            if n.fg :
                f.enfiler(n.fg)
            if n.fd :
                f.enfiler(n.fd)
            print(n.info, end=' ')      # on traite le noeud

    def rechercherElement(self, elmt) :
        """Retourne un couple (bool, abr) où bool indique si l'élément est présent 
        dans l'arbre et abr est None ou un objet de la classe Arbre"""
        if not self.info :
            return (False, None)
        if elmt == self.info:
            return (True, self)
        if elmt < self.info and self.fg :             
            return self.fg.rechercherElement(elmt)
        if elmt > self.info and self.fd :
            return self.fd.rechercherElement(elmt)
        return (False, None)
    
    def rechercherElementIteratif(self, elmt) :
        """retourne un tuple dont le premier élément est un booléen indiquant si l’élément 
        est présent et le deuxième le noeud de l’arbre où il est présent (None si absent)"""
        if not self.info :
            return (False, None)
        while self and self.info != elmt :
            if elmt < self.info :
                self = self.fg
            else :
                self = self.fd
        if self is None :
            return (False, None)
        else :
            return (True, self)  

    def hauteurArbre(self) : 
        """Retourne la hauteur d'un arbre : attention, un noeud feuille est de hauteur 0 !"""
        if not self.info :
            return -1
        h = -1
        if self.fg and self.fd :
            h = max(self.fg.hauteurArbre(), self.fd.hauteurArbre())
        elif self.fg :
            h= self.fg.hauteurArbre()
        elif self.fd :
            h = self.fd.hauteurArbre()
        return 1+h

    def __eq__(self, other) : 
        assert isinstance(other, type(self)), "éléments de types différents"
        #si les noeuds n'ont pas la même valeur ou pas la même structure de filiation
        if self.info != other.info or (self.fg and not other.fg) or (not self.fg and other.fg) \
                                   or (self.fd and not other.fd) or (not self.fd and other.fd) :
            return False
        #ici on a l'égalité et la même structure de filiation
        #premier sous-cas :si les deux noeuds sont vides alors ils sont égaux
        #si self.info à None, on a forcement other.info à None sinon on aurait retourner False précédemment
        #de plus on a forcément self.fd et self.fg à None (noeud vide dont on renvoie Vrai)
        if self.info is None :
            return True
        #deuxième sous-cas si les noeuds ont même valeur alors les arbres sont égaux ssi les fils g et d égaux
        return self.fg == other.fg and self.fd == other.fd

    def estBinaireDeRecherche(self) :
        if self.info is None or not self.fg and not self.fg :      #noeud feuille ou None
            return True
        if self.fg and not self.fd and self.fg.info < self.info :  #un seul fils à g
            return self.fg.estBinaireDeRecherche()
        if self.fd and not self.fg and self.fd.info > self.info :  #un seul fils à d
            return self.fd.estBinaireDeRecherche()
        if self.fd and self.fg and self.fg.info < self.info < self.fd.info :
            return self.fg.estBinaireDeRecherche() and self.fd.estBinaireDeRecherche()

    def brancheMaxGloutonne(self) :
        """On fait le choix glouton localement optimal du noeud de valeur maximale à chaque niveau, donc à droite !!
        Clairement ce n'est pas globalement optimal, non optimal quand très peu de valeurs à dte !!
        Complexité : hauteur de l'arbre O(n) pour arbre dégénéré (pire cas) on parcourt chq noeud et on fait n sommes"""
        somme = 0
        while self :
            somme += self.info
            if self.fd :
                self = self.fd
            elif self.fg :
                self = self.fg
            else :
                self = None
        return somme

    def brancheMaxOptimale(self) :
        #valeur maximale d'une branche en programmation dynamique
        """La programmation dynamique est une technique pour résoudre des problèmes algorithmiques  
        qui consiste à les séparer en sous-problèmes qui suivent une sous-structure optimale.
        Elle peut s’en servir pour calculer efficament des quantités définies récursivement.
        Sur un arbre, l’idée est d’associer une valeur à chaque noeud qui combine les valeurs de ces fils.
        Donner une version en programmation dynamique (donc optimale) de l’algorithme précédent.
        Quelle est sa complexité ?  nombre de noeuds de l'arbre  """
        if not self.info :
            return 0
        if self.fg and self.fd :
            brancheMax = max(self.fg.brancheMaxOptimale(), self.fd.brancheMaxOptimale())
        elif self.fg :
            brancheMax = self.fg.brancheMaxOptimale()
        elif self.fd :
            brancheMax = self.fd.brancheMaxOptimale()
        else :
            brancheMax = 0
        return self.info + brancheMax   

    def plusGrandPredecesseur(self) :
        """Retourne le noeud de plus grande valeur < a racine et son parent"""
        #pour prendre le plus proche predecesseur, on va le plus loin possible sur la droite du files gauche
        if not self.info :
            return
        parent = self
        self =self.fg
        if self :                         
            while self.fd :
                parent = self
                self = self.fd
        print('ppp ', self.info,'parent ', parent.info)
        return self, parent        
    
    def plusPetitSuccesseur(self) :
        """Retourne le noeud de plus petite valeur > a raine et son parent"""
        #pour prendre le plus proche successeur, on va le plus loin possible sur la gauche du fils droit
        if not self.info :
            return
        parent = self
        self =self.fd
        if self :                         
            while self.fg :
                parent = self
                self = self.fg
        print('pps ',self.info,'parent ', parent.info)
        return self, parent               
    
    def supprimerElement(self, elmt, parent = None) :
        if not self.info :  
            return
        # si elmt est inférieur à la valeur du self, rechercher dans le sous-arbre gauche
        if elmt < self.info and self.fg :         #à mettre sinon supprime elmt non present ne marche pas ???
            self.fg.supprimerElement(elmt, self)
        # si elmt est sépérieur à la valeur du self, rechercher dans le sous-arbre droit
        elif elmt > self.info and self.fd  :
            self.fd.supprimerElement(elmt, self)
        elif elmt == self.info : #On a trouvé l'élément à supprimer
            # ne pas mettre else car element peut etre pas present !!
            # si self est une feuille (n'a pas d'enfant !)
            if not self.fg and not self.fd :
                #si ce n'est pas le noeud racine, son parent doit pointer sur None
                if parent :
                    if parent.fg is self:
                        parent.fg = None
                    else:
                        parent.fd = None
                #si c'est le noeud racine, pa de parent : mettre juste sa valeur à self.
                else :
                    self.info = None               
            # self a un fils unique à doite
            elif not self.fg :  #donc self.fd is not Nune...
                #si ce n'est pas le noeud racine, son parent doit pointer sur le fils unique fd
                if parent :
                    if parent.fg is self:
                        parent.fg = self.fd
                    else:
                        parent.fd = self.fd
                #cas du noeud racine
                else: 
                    self.info = self.fd.info
                    self.fd = self.fd.fd
                    self.fg = self.fd.fg
            # self a un fils unique à gauche
            elif not self.fd :  #donc self.fg is not None...
                #si ce n'est pas le noeud racine, son parent doit pointer sur le fils unique fg
                if parent :
                    if parent.fg is self:
                        parent.fg = self.fg
                    else:
                        parent.fd = self.fg
                #cas du noeud racine
                else: 
                    self.info = self.fg.info
                    self.fd = self.fg.fd
                    self.fg = self.fg.fg
            # self a deux fils
            else :
                # il faut remplacer la valeur de self par celle de son plus proche predecesseur/successeur ppp/pps  
                # on alterne pour équilibrer ???
                if randint(0,1) == 1:
                    #remplacement par le plus proche prédécesseur
                    print('plus proche predécésseur')
                    (pred, parentpred) = self.plusGrandPredecesseur()
                    #si le ppprédécesseur a un fils gauche (au pire None)
                    #de toute manière, il ne peut pas avoir de fils droit : + gd pred !!
                    #le parent de ce pppredecesseur doit pointer sur fils gauche, et c'est souvent parent.fd
                    #mais si on est tt de suite après la racine, c'est le parent.fg !!
                    if parentpred.fg is pred :
                        parentpred.fg = pred.fg                        
                    else:
                        parentpred.fd = pred.fg 
                    #on insère le plus proche prédécesseur à la place du noeud
                    
                    #cas où self est le noeud racine
                    if parent is None:
                        self.info = pred.info
                    #si ce n'est pas le noeud racine, son parent doit pointer sur le fils unique fg
                    else:
                        #sinon si self est un fils gauche
                        if parent.fg is self :
                            parent.fg = pred                        
                        else:
                            parent.fd = pred
                        #le  plus proche prédécesseur hérite des fils de self
                        pred.fg = self.fg
                        pred.fd = self.fd                        
                else :
                    #remplacement par le plus proche successeur
                    print('plus proche successeur')
                    (succ, parentsucc) = self.plusPetitSuccesseur()
                    #si le ppsuccesseur a un fils droit (au pire None)
                    #de toute manière, il ne peut pas avoir de fils gauche : + petit succ !!
                    #le parent de ce ppsuccesseur doit pointer sur fils droit, et c'est souvent parent.fg
                    #mais si on est tt de suite après la racine, c'est le parent.fd !!
                    if parentsucc.fg is succ :
                        parentsucc.fg = succ.fd                        
                    else:
                        parentsucc.fd = succ.fd
                    #on insère le plus proche prédécesseur à la place du noeud
                    
                    #cas où self est le noeud racine
                    if parent is None :
                        self.info = succ.info
                    #si ce n'est pas le noeud racine, son parent doit pointer sur le fils unique fg
                    else:
                        #sinon si self est un fils gauche
                        if parent.fg is self :
                            parent.fg = succ                        
                        else:
                            parent.fd = succ
                        #le  plus proche prédécesseur hérite des fils de self
                        succ.fg = self.fg
                        succ.fd = self.fd                     

    def vider(self) :
        pass
    
    def __del__(self) :
        pass 

    def estFeuille(self) :
        return self.info != None and not self.fg and not self.fd

    def degre(self) :
        pass


print('###############      tests de Brig    ####################')

a1 = Arbre()   # arbre vide
print('arbre vide')
a1.afficherParcoursInfixe()
print()
print('est-il vide ? ', a1.estVide())
print('hauteur arbre : ',a1.hauteurArbre())
print('est-ce une feuille : ',a1.estFeuille())
print()
a2 = Arbre(2)  # arbre avec un noeud (la racine)
print('arbre avec le noeud 2')
a2.afficherParcoursInfixe()
print()
print('est-il vide ? ', a2.estVide())
print('hauteur arbre : ',a2.hauteurArbre())
print('est-ce une feuille : ',a2.estFeuille())
print()
print('les différents affichages')
a = Arbre() # arbre vide
a.insererElement(5) # ajout d’un noeud valant 5 à la racine
a.insererElement(2) # ajout d’un noeud valant 2 en fct de la racine
a.insererElement(7) # ajout d’un noeud valant 7 en fct des autres
a.insererElement(9) # ajout d’un noeud valant 9 en fct des autres
a.insererElement(3) # ajout d’un noeud valant 3 en fct des autres
a.insererElement(8) # ajout d’un noeud valant 8 en fct des autres
a.insererElement(6) # ajout d’un noeud valant 6 en fct des autres
a.insererElement(1) # ajout d’un noeud valant 1 en fct des autres
a.insererElement(4) # ajout d’un noeud valant 4 en fct des autres
print('infixe : ')
a.afficherParcoursInfixe()
print()   # 1 2 3 4 5 6 7 8 9
print('préfixe : ')
a.afficherParcoursPrefixe()
print()   # 5 2 1 3 4 7 6 9 8
print('péfixe_iter : ')
a.afficherParcoursPrefixeIteratif()
print()   # 5 2 1 3 4 7 6 9 8
print('postfixe : ')
a.afficherParcoursPostfixe()
print()   # 1 4 3 2 6 8 9 7 5
print('largeur : ')
a.afficherParcoursLargeur()
print()   # 5 2 7 1 3 6 9 4 8
print()
print('hauteur arbre : ',a.hauteurArbre())
print('est-ce une feuille : ',a.estFeuille())
print()
print('recherche recursive')
print('4 present ?')
print(a.rechercherElement(4))
print('0 present ?')
print(a.rechercherElement(0))
print()
print('recherche iterative')
print('4 present ?')
print(a.rechercherElementIteratif(4))
print('0 present ?')
print(a.rechercherElementIteratif(0))
print()
print('égalité')
b = Arbre()
b.insererElement(5) 
b.insererElement(2) 
b.insererElement(7) 
b.insererElement(9) 
b.insererElement(3)
c = Arbre()
c.insererElement(7) 
c.insererElement(5) 
c.insererElement(3) 
c.insererElement(9) 
c.insererElement(2)
print(b == a)   #False
print(b == b)   #True
print(b == c)   #False
print(b == a1)  #False
print(a1 == a1) #True
print()
print('arbre binaire de recherche ? ', a.estBinaireDeRecherche())
print()
print('branche maximale gloutonne arbre a : ', a.brancheMaxGloutonne())
print('branche maximale gloutonne arbre b : ', b.brancheMaxGloutonne())
print('branche maximale gloutonne arbre c : ', c.brancheMaxGloutonne())
print("non optimale car pour c c'est pas 16 mais 17 !! cas quand très peu de valeur à dte !!")
print('branche maximale optimale arbre a : ', a.brancheMaxOptimale())
print('branche maximale optimale arbre b : ', b.brancheMaxOptimale())
print('branche maximale optimale arbre c : ', c.brancheMaxOptimale())
print()
a.affichage()
print('supression')
print('supprime 5')
a.supprimerElement(5)  #en plein milieu avec sucesseur...
a.affichage()
print('arbre binaire de recherche ? ', a.estBinaireDeRecherche())
print('supprime 0')
a.supprimerElement(0)
a.affichage()
print('supprime 1')
a.supprimerElement(1)  #suppr feuille...
a.affichage()
a.afficherParcoursPrefixe()
print()
print('supprime 2')
a.supprimerElement(2)  #suppr noeud avec fils unique
a.affichage()

print()
print()
print('###############      tests de Fred    ####################')
arbre = Arbre()
for k in [5,2,3,1,7,8]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre.insererElement(k)
    print("Affichage parcours infixe")
    arbre.afficherParcoursInfixe()
    print()
    print("Affichage parcours préfixe")
    arbre.afficherParcoursPrefixe()
    print()
    print("Affichage parcours préfixe itératif")
    arbre.afficherParcoursPrefixeIteratif()
    print()
    print("Affichage parcours postfixe")
    arbre.afficherParcoursPostfixe()
    print()
    print("Affichage parcours en largeur")
    arbre.afficherParcoursLargeur()
    print()
print("Hauteur : ", arbre.hauteurArbre())
arbre.affichage()
print("Recherche d'élément")
for k in [5,2,3,1,7,8, 9]:
    print(f"{k} dans arbre : ", arbre.rechercherElement(k))
print("Recherche itérative d'élément")
for k in [5,2,3,1,7,8, 9]:
    print(f"{k} dans arbre : ", arbre.rechercherElementIteratif(k))
print("Construction d'un arbre 2 avec les mếmes valeurs insérées dans le même ordre")
arbre2 = Arbre()
for k in [5,2,3,1,7,8]:
    arbre2.insererElement(k)
print(f"arbre == arbre2, {arbre == arbre2}")
print("Insertion d'une autre valeur 9 dans arbre 2")
arbre2.insererElement(9)
print(f"arbre == arbre2, {arbre == arbre2}")
print("Affichage parcours en largeur de arbre2")
arbre2.afficherParcoursLargeur()
print()
print("Construction d'un arbre 3  avec les mếmes valeurs que dans arbre mais insérées dans le désordre")
arbre3 = Arbre()
for k in reversed([5,2,3,1,7,8]):
    arbre3.insererElement(k)
print(f"arbre == arbre3, {arbre == arbre3}")
print("Affichage parcours en largeur de arbre3")
arbre3.afficherParcoursLargeur()
print()
arbre4 = Arbre()
for k in [5,3,4,1,6]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre4.insererElement(k)
arbre4.afficherParcoursPrefixe()
print()
print("Branche maximale glouton d'arbre non optimale")
print(arbre4.brancheMaxGloutonne())
print("Branche maximale dynamique d'arbre (optimale)")
print(arbre4.brancheMaxOptimale())

print("Suppression d'éléments")
print("Suppression d'une feuille")
arbre4.supprimerElement(1, None)
print("Affichage parcours préfixe")
arbre4.afficherParcoursPrefixe()
print("Suppression d'un élément avec un fils")
arbre4.supprimerElement(3, None)
print("Affichage parcours préfixe")
arbre4.afficherParcoursPrefixe()
print("Réinsertion des éléments supprimés")
arbre4.insererElement(3)
arbre4.insererElement(1)
print("Affichage parcours préfixe")
arbre4.afficherParcoursPrefixe()
print("Suppression d'un élément avec deux fils")
arbre4.supprimerElement(3, None)
print("Affichage parcours préfixe")
arbre4.afficherParcoursPrefixe()

arbre5 = Arbre()
for k in [5,3,4,1,7,6,2]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre5.insererElement(k)
arbre5.affichage()
print()
print("Branche maximale glouton d'arbre non optimale")
print(arbre5.brancheMaxGloutonne())
print("Branche maximale dynamique d'arbre (optimale)")
print(arbre5.brancheMaxOptimale())
print("Suppression d'éléments")
print("Suppression d'une feuille", 2)
arbre5.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression d'un élément avec un fils", 7)
arbre5.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Réinsertion des éléments supprimés")
arbre5.insererElement(2)
arbre5.insererElement(7)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression d'un élément avec deux fils", 3)
arbre5.supprimerElement(3, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression de la racine ", 5)
arbre5.supprimerElement(5, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression du noeud", 2)
arbre5.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression du noeud", 4)
arbre5.supprimerElement(4, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression du noeud", 1)
arbre5.supprimerElement(1, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression du noeud", 7)
arbre5.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre5.affichage()
print("Suppression du noeud", 6)
arbre5.supprimerElement(6, None)
print("Affichage parcours préfixe")
arbre5.affichage()
