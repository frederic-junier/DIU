
# coding: utf-8

# ## Classe Pile

# In[3]:


class Pile:
    """à partir d'un tableau dynamique en Python"""
    
    def __init__(self, liste):
        self.liste = liste
        
    def __str__(self):
        output = ''
        for e in reversed(self.liste):
            output += "|{:^15}|\n".format(e)
            output += "|{:^15}|\n".format('_'*15)
        return output
    
    def __repr__(self):
        return repr(self.liste)
        
    def depiler(self):
        assert not self.estVide(), "La pile est vide !"
        self.liste.pop()
    
    def empiler(self, e):
        self.liste.append(e)
        
    def estVide(self):
        return self.liste == []
        #return len(self.liste) == 0 #non sinon on utiliserait len pour la hauteur
    
    def sommet(self):
        assert not self.estVide(), "La pile est vide !"
        return self.liste[-1]
    
    def traiter(self):
        assert not self.estVide(), "La pile est vide !"
        element = self.sommet()
        #return self.liste.pop()
        self.depiler()
        return element
        
    
    def hauteur(self):
        pile2 = Pile([])
        compteur = 0
        #on utilise est_vide 
        #donc il ne faut pas utiliser hauteur dans est_vide
        while not self.estVide(): 
            pile2.empiler(self.traiter())
            compteur += 1
        #on reconstruit la pile
        while not pile2.estVide():
            self.empiler(pile2.traiter())
        return compteur
    
    def __len__(self):
        return self.hauteur()
    
    def vider(self):
        while not self.estVide():
            self.depiler()
    
    def __del__(self):
        self.vider()
        print(f"destruction de {repr(self)}")        


# ## Classe File

# In[4]:


class File:
    """à partir d'un tableau dynamique en Python"""
    
    def __init__(self, liste):
        self.liste = liste
        
    def __str__(self):
        output = 'Tếte : '
        for e in  self.liste:
            output += "{:^15}<--".format(e)
        return output.rstrip('<--') + ': Queue'
    
    def __repr__(self):
        return repr(self.liste)
        
    def defiler(self):
        assert not self.estVide(), "La file est vide !"
        self.liste.pop(0)
    
    def enfiler(self, e):
        self.liste.append(e)
        
    def estVide(self):
        return self.liste == []
        #return len(self.liste) == 0 #non sinon on utiliserait len pour la hauteur
    
    def premierDeLaFile(self):
        assert not self.estVide(), "La file est vide !"
        return self.liste[0]
    
    def traiter(self):
        assert not self.estVide(), "La pile est vide !"
        element = self.premierDeLaFile()
        #return self.liste.pop()
        self.defiler()
        return element
        
    
    def longueur(self):
        file2 = File([])
        compteur = 0
        #on utilise est_vide 
        #donc il ne faut pas utiliser hauteur dans est_vide
        while not self.estVide(): 
            file2.enfiler(self.traiter())
            compteur += 1
        #on reconstruit la file
        while not file2.estVide():
            self.enfiler(file2.traiter())
        return compteur
    
    def __len__(self):
        return self.longueur()
    
    def vider(self):
        while not self.estVide():
            self.defiler()
    
    def __del__(self):
        self.vider()
        print(f"destruction de {repr(self)}")


# ## Classe arbre binaire de recherche 

# ![api-arbre](api-arbre.png)

# ![implementation-arbre.png](implementation-arbre.png)

# Applications des ABR :
# 
# 
# * Pour stocker des éléments triés : quel parcours nous donne les valeurs valeurs triées dans un ordre (parcours infixe pour un ABR) ? 
# * Même intérêt que les listes triées, avec en plus des informations de la structure Arbre (père, fils ...)
# * On peut créer une classe Arbre dont on fait hériter la classe ABR mais pas l'inverse
# * On peut même envisager de créer une classe d'Arbres naire puis la dériver en Arbre puis en Arbre binaire
# 
# 
# Ce qu'il faut maitriser pour le programme de NSI de terminale :
# 
# * le vocabulaire
# * identifier des situations où il est intéressant d'utiliser un arbre
# * algorithmes sur les arbres/arbres binaires, les parcours, la recherche, l'insertion d'un élément dans un ABR
# * bien repérer que la structure de données est hautement récursive
# * permet de faire de la POO
# * lorsque l'ABR est équilibré on a le meilleur cout possible pour insérer ou rechercher un élément dans un arbre qui est en log2(n)
#     
#     

# In[13]:


from random import randint



class ABR:
    
    def __init__(self, info = None, fg = None, fd = None):
        self.info = info
        self.fg = None
        self.fd = None
        
    def estVide(self):
        return self.info is None
    
    #proposition de Pascal Salliot
    def affichage(self, niveau=0, c=132):
        if self.fd:
            self.fd.affichage( niveau+1, 47 )
        print(f"{4 * niveau * ' '}{chr(c)}{self.info}")
        if self.fg:
            self.fg.affichage( niveau+1, 92 )
            
    def afficherArbre(self):
        if not self.info: return
        h = self.hauteur()
        f = File([])
        ind_racine = ((2 ** h) * 2 - 2) // 2
        decalage = (2 ** h)
        f.enfiler((self, ind_racine, decalage))
        liste = []
        liste.append((self, ind_racine, decalage))
        while not f.estVide():
            (n, i, d) = f.traiter()
            if n.fg:
                f.enfiler((n.fg, i - d // 2, d // 2))
                liste.append((n.fg, i - d // 2, d // 2))
            if n.fd:
                f.enfiler((n.fd, i + d // 2, d // 2))
                liste.append((n.fd, i + d // 2, d // 2))
        (n, i, d) = liste[0]
        for _ in range(d - 2):
            print(' ', end='')
        print(str(n.info), end='')
        (nprec, iprec, dprec) = (n, i, d)
        for (n, i, d) in liste[1:]:
            if d != dprec:
                print()
                iprec = -1
            for _ in range(i - iprec - 1):
                print(' ', end='')
            print(str(n.info), end='')
            (nprec, iprec, dprec) = (n, i, d)  
            
            
    def insererElement(self, e):
        #if not self.estVide(): 
        #bien pour le jour où on change de façon de représenter un arbre vide
        #cout de refactoring réduit si on utilise est_vide
        if self.info is None: #cas d'un arbre vide
            self.info  = e
        elif e < self.info: #insertion dans le sous-arbre gauche
            if self.fg is not None:
                self.fg.insererElement(e)
            else:
                self.fg = ABR(info = e)
        elif e > self.info:  #insertion dans le sous-arbre droit
            if self.fd is not None:
                self.fd.insererElement(e)
            else:
                self.fd = ABR(info = e)
        #rien à faire si e == self.info on arrête la récursion
        #et on n'insère pas e dans l'arbre
    
    def afficherParcoursInfixe(self):
        if self.info is not None: #si l'arbre est non  vide
            if self.fg is not None:
                self.fg.afficherParcoursInfixe()
            print(self.info)
            if self.fd is not None:
                self.fd.afficherParcoursInfixe()
                
    def afficherParcoursPrefixe(self):
        if self.info is not None: #si l'arbre n'est pas vide
            print(self.info)
            if self.fg is not None:
                self.fg.afficherParcoursPrefixe()            
            if self.fd is not None:
                self.fd.afficherParcoursPrefixe() 
                
    def afficherParcoursPostfixe(self):
        if self.info is not None: #si l'arbre n'est pas vide          
            if self.fg is not None:
                self.fg.afficherParcoursPostfixe()            
            if self.fd is not None:
                self.fd.afficherParcoursPostfixe() 
            print(self.info)
            
    def afficherParcoursLargeur(self):
        if self.info is not None: #si l'arbre n'est pas vide
            queue = File([])
            queue.enfiler(self)
            while not queue.estVide():
                noeud = queue.traiter()
                if noeud.fg is not None:
                    queue.enfiler(noeud.fg)
                if noeud.fd is not None:
                    queue.enfiler(noeud.fd)
                print(f'noeud de valeur {noeud.info} traité')
                repr(queue)
                    
    def rechercheElement(self, e):
        """Retourne un couple (booléen, abr)
        où booleen indique si l'élément est présent dans l'arbre
        et abr est None ou un objet de la classe ABR"""
        if self.info is None:
            return (False, None)
        elif self.info == e:
            return (True, self)
        elif self.info > e:
            if self.fg is not None:
                return self.fg.rechercheElement(e)
            return (False, None)
        else:
            if self.fd is not None:
                return self.fd.rechercheElement(e)
            return (False, None)
    
    def hauteur(self):
        """Retourne la hauteur d'un arbre """
        if self.info is None: #si l'arbre est vide
            return -1
        else:
            h = 0
            #cas de base d'une feuille
            if self.fg is  None and self.fd is  None:
                return h
            #on a un sous-arbre gauche
            if self.fg is not None:
                h = max(h, self.fg.hauteur())
            #on a un sous-arbre droit
            if self.fd is not None:
                h = max(h, self.fd.hauteur())  
            #on retourn le maximum des hauteurs des sous-arbres + 1 (arêtes reliant self aux sous-arbres)
            return 1 + h     
        
    def hauteurArbre(self):
        """Version de Nicolas Pronost"""
        if not self.info: return -1
        hgauche = self.fg.hauteurArbre() if self.fg else -1
        hdroit = self.fd.hauteurArbre() if self.fd else -1
        if hgauche > hdroit:
            return hgauche + 1
        else:
            return hdroit + 1
        
    def parcoursPrefixeIteratif(self):
        if self.info is not None: #si l'arbre n'est pas vide 
            stack = Pile([])
            stack.empiler(self)  #on empile la racine
            while not stack.estVide():
                noeud = stack.traiter() #on récupère le noeud
                print(noeud.info)       #on l'affiche (parcours préfixe)
                if noeud.fd is not None:
                    stack.empiler(noeud.fd) #on empile le fils droit (traité après)
                if noeud.fg is not None:
                    stack.empiler(noeud.fg) #on empile le fils gauche (traité avant)
                
    def __eq__(self, other):
        assert isinstance(other, type(self)), "éléments de types différents"
        if self.info is None: #si l'arbre est vide
            return other.info is None #on test si l'autre arbre est vide
        else: #on fait un parcours préfixe en parallèles des deux arbres et on compare les noeuds
            #Premier cas : les valeurs du noeud courant et de l'autre sont différentes
            print(self.info, other.info)
            if self.info != other.info: #si les noeuds sont différents (traite le cas où other.info == none)
                return False
            #Second cas : self une feuille
            if  self.fg is None and self.fd is None:
                #on teste si l'autre est aussi une feuille
                return other.fg is None and other.fd is None
            #3eme cas : self.info = other.info et self a au moins un fils
            rep = True
            #3eme cas, premier sous-cas: on compare le fils gauche du noeud courant avec celui de l'autre
            if self.fg is not None:   #si le noeud a un fils gauche, on compare les fils gauches
                if other.fg is not None: #si l'autre noeud a aussi un fils gauche
                    rep = rep and self.fg.__eq__(other.fg)
                else:
                    return False
            #3eme cas, second sous-cas  :  on compare le fils droit du noeud courant avec celui de l'autre
            if self.fd is not None:  #si le noeud a un fils droit, on compare les fils droits
                if other.fd is not None: #si l'autre noeud a aussi un fils droit
                    rep = rep and  self.fd.__eq__(other.fd)
                else:
                    return False
            #Retour de la réponse du 3eme cas
            return rep
        
    def egalite(self , other):
        assert isinstance(other, type(self)), "éléments de types différents"
        #si les noeuds n'ont pas la même valeur ou pas la même structure de filiation
        if self.info != other.info or (self.fg and not other.fg) or (not self.fg and other.fg)                                    or (self.fd and not other.fd) or (not self.fd and other.fd) :
            return False
        #ici on a l'égalité et la même structure de filiation
        #premier sous-cas :si les deux noeuds sont vides alors ils sont égaux
        #si self.info à None, on a forcement other.info à None sinon on aurait retourner False précédemment
        #de plus on a forcément self.fd et self.fg à None (noeud vide dont on renvoie Vrai)
        if self.info is None : 
            return True
        #deuxième sous-cas si les noeuds ont même valeur alors les arbres sont égaux ssi les fils g et d égaux
        return self.fg == other.fg and self.fd == other.fd
    
    

    def rechercheIterativeElement2(self, e):
        """retourne un tuple dont le premier élément est un booléen indiquant si l’élément est présent
        et le deuxième le noeud de l’arbre où il est présent (None si absent).
        Maladroit parce qu'on n'utilise pas la propriété d'ABR, une pile est inutile"""
        if self.info is None:
            return (False, None)
        else:
            stack = Pile([])
            stack.empiler(self)  #on empile la racine
            while not stack.estVide():
                noeud = stack.traiter() #on récupère le noeud
                if noeud.info == e:
                    return (True, noeud)
                if noeud.fd is not None:
                    stack.empiler(noeud.fd) #on empile le fils droit (traité après)
                if noeud.fg is not None:
                    stack.empiler(noeud.fg) #on empile le fils gauche (traité avant)
            #pile vide et noeud jamais trouvé
            return (False, None)
        
    def rechercheIterativeElement(self, e):    
        """retourne un tuple dont le premier élément est un booléen indiquant si l’élément est présent
        et le deuxième le noeud de l’arbre où il est présent (None si absent)"""
        if not self.info :
            return (False, None)
        while self and self.info != e :
            if e < self.info :
                self = self.fg
            else :
                self = self.fd
        if self is None :
            return (False, None)
        else :
            return (True, self)  
        
    @staticmethod    #cela me semble bizarre que ce soit une méthode de la classe ABR
    def estABR2(self):
        #Premier cas : arbre vide
        if self.info is None: 
            return True         
        res = True
        #Deuxième cas : un fils gauche existe, la valeur de sa racine doit être inférieure à self.info
        # et de doit être ABR
        if self.fg is not None:
            #j'ajoute un test  au cas où on ajouterait des arbres vides comme fils d'une feuille
            res =  res and self.fg.info is not None and self.fg.info < self.info and self.fg.estABR()
        #Troisième cas : un fils droite existe, la valeur de sa racine doit être supérieure à self.info
        # et ce doit être un ABR
        if self.fd is not None:
            res = res and self.fd.info is not None and self.fd.info > self.info and self.fd.estABR()
        return res
    
    def estABR(self):
        #Premier cas : arbre vide
        if self.info is None: 
            return True         
        res = True
        #Deuxième cas : un fils gauche existe, la valeur de sa racine doit être inférieure à self.info
        # et de doit être ABR
        if self.fg is not None:    
            res =  res  and self.fg.info < self.info and self.fg.estABR()
        #Troisième cas : un fils droite existe, la valeur de sa racine doit être supérieure à self.info
        # et ce doit être un ABR
        if self.fd is not None:
            res = res  and self.fd.info > self.info and self.fd.estABR()
        return res
    

    def est_ABR(self, mini = float('-inf'), maxi = float('+inf')):
        """Version de Pierre,
        Teste si self est un ABR dont les noeuds sont strictement compris
        entre mini et maxi"""

        if self.info is None:
            return True
        if not mini < self.info < maxi:
            return False
        gauche = (self.fg == None) or self.fg.est_ABR(mini, self.info)
        droite = (self.fd == None) or self.fd.est_ABR(self.info, maxi)
        return gauche and droite
    """
    pour vérifier que c'est un ABR
    il suffit des faire un parcours infixe
    et de vérifier que la liste des noeuds est bien ordonnée    
    """
    
    def estABR(self):
        #Premier cas : arbre vide
        if self.estVide(): 
            return True  
        (test, min, max) = self.__estABRSousArbre()
        return test
    
    def __estABRSousArbre(self):
        minG = maxG = minD = maxD = self.info
        testG = testD = True
        if self.fg:(testG, minG, maxG) = self.fg.__estABRSousArbre()
        if self.fd:(testD, minD, maxD) = self.fd.__estABRSousArbre()
        if not testG or not testD: return (False, None, None)
        if maxG > self.info or minD < self.info: return (False, None, None)
        return (True, minG, maxD)
    
     #valeur maximale d'une branche
    def brancheMaximaleGlouton(self):
        """On fait le choix glouton localement optimal du noeud de valeur maximale à chaque niveau
        Clairement ce n'est pas globalement optimal
        Complexité : hauteur de l'arbre
        Fonctionne pour des arbres quelconques a priori
        """
         #Premier cas : arbre vide
        if self.info is None: 
            return 0
        vmax = -float('inf')
        suivant = None
        if self.fg:
            vmax = self.fg.info
            suivant = self.fg
        if self.fd:
            if self.fd.info > vmax:
                vmax = self.fd.info
                suivant = self.fd
        if suivant is not None:
            return self.info + suivant.brancheMaximaleGlouton()
        else:
            return  self.info 
        
    def brancheMaximaleGlouton2(self) :
        """Attention ne fonction que pour des ABR"""
         #Premier cas : arbre vide
        if self.info is not  None: 
            somme = 0
            while self:
                somme += self.info
                if self.fd :
                    self = self.fd
                elif self.fg :
                    self = self.fg
                else :
                    self = None
            return somme
        
    """
    La programmation dynamique est une technique pour résoudre des problèmes algorithmiques qui consiste à les
    séparer en sous-problèmes qui suivent une sous-structure optimale. Elle peut s’en servir pour calculer efficament
    des quantités définies récursivement. Sur un arbre, l’idée est d’associer une valeur à chaque noeud qui combine les
    valeurs de ces fils.
    Donner une version en programmation dynamique (donc optimale) de l’algorithme précédent. Quelle est sa
    complexité ?
    """

    #valeur maximale d'une branche en programmation dynamique
    def brancheMaximaleDynamique(self):
        """Complexité : nombre de noeuds de l'arbre
        Fonctionne pour des arbres quelconques        
        """
         #Si l'arbre n'est pas vide
        if self.info is not  None:              
            brancheMax = -float('inf')
            if self.fg is not None:
                brancheMax = max(brancheMax, self.fg.brancheMaximaleDynamique())
            if self.fd is not None:
                brancheMax  = max(brancheMax, self.fd.brancheMaximaleDynamique())
            if self.fg is  None and self.fd is None:
                #print("retour", self.info)
                return  self.info
            return self.info + brancheMax
        
    
    def maxBrancheProgDyn(self):
        """Solution de Nicolas Pronost"""
        if self.estVide(): return None
        sum_fg = self.info if self.fg is None else self.info + self.fg.maxBrancheProgDyn()
        sum_fd = self.info if self.fd is None else self.info + self.fd.maxBrancheProgDyn()
        return max(sum_fg, sum_fd)
    
    def noeudMax(self, parent = None):
        """Retourne le noeudMax et son parent"""
        if self.info is not None: #si l'arbre est non vide
            if self.fd is not None:
                return self.fd.noeudMax(self)
            return (self, parent)
    
    def noeudMin(self, parent = None):
        """Retourne le noeudMin et son parent"""
        if self.info is not None: #si l'arbre est non vide
            if self.fg is not None:
                return self.fg.noeudMin(self)
            return (self, parent)
        
    def plusGrandPredecesseur(self):
        """Retourne le noeud de plus grande valeur < """
        if self.info is not None: #si l'arbre est non vide
            if self.fg is not None:
                return self.fg.noeudMax(self)
            return (self, self)
    
    def plusGrandPredecesseur2(self):
        """Retourne le noeud de plus grande valeur < et son parent"""
        if self.info is not None: #si l'arbre est non vide
            if self.fg is None:
                return (self, self)
            parent = self
            fils = self.fg
            while fils.fd is not None:
                parent, fils = fils, fils.fd
            return (fils, parent)
        
    
    def plusPetitSuccesseur(self):
        """Retourne le noeud de plus petite valeur > """
        if self.info is not None: #si l'arbre est non vide
            if self.fd is not None:
                return self.fd.noeudMin(self)
        return (self, self)
    
    def plusPetitSuccesseur2(self):
        """Retourne le noeud de plus grande valeur > et son parent"""
        if self.info is not None: #si l'arbre est non vide
            if self.fd is None:
                return (self, self)
            parent = self
            fils = self.fd
            while fils.fg is not None:
                parent, fils = fils, fils.fg
            return (fils, parent)
        
    def supprimerElement(self, e, parent = None):
        #Premier cas : arbre vide
        if self.info is None: 
            return  #rien à faire
        #on a trouvé l'élément
        if self.info == e:
            #premier cas c'est une feuille
            if self.fg is None and self.fd is None:
                #si ce n'est pas le noeud racine
                if parent is not None:
                    if parent.fg is self:
                        parent.fg = None
                    else:
                        parent.fd = None
                else: #sinon on supprime la valeur du noeud
                    self.info = None
            #second cas un seul fils: le fils gauche
            elif self.fg is not None and self.fd is None:
                #si ce n'est pas le noeud racine
                if parent is not None:
                    if parent.fg is self:
                        parent.fg = self.fg
                    else:
                        parent.fd = self.fg
                else: #cas du noeud racine
                    self.info = self.fg.info
                    self.fd = self.fg.fd
                    self.fg = self.fg.fg
            #second cas bis un seul fils: le fils droit
            elif self.fg is  None and self.fd is not None:
                #si ce n'est pas le noeud racine
                if parent is not None:
                    if parent.fg is self:
                        parent.fg = self.fd
                    else:
                        parent.fd = self.fd
                else: #cas du noeud racine
                    self.info = self.fd.info
                    self.fg = self.fd.fg
                    self.fd = self.fd.fd
            #3eme cas : le noeud a deux fils:
            else: 
                if randint(0, 1) == 1:
                    #remplacement par le plus proche prédécesseur
                    (predec, parentpredec) = self.plusGrandPredecesseur()
                    #si le plus proche prédécesseur a un fils gauche
                    #on détache le  plus proche prédécesseur
                    #et on attache son fils à son père
                    if parentpredec.fg is predec:
                        parentpredec.fg = predec.fg                        
                    else:
                        parentpredec.fd = predec.fg 
                    #on insère le  plus proche prédécesseur à la place du noeud
                    #cas où self est le noeud racine
                    if parent is None:
                        self.info = predec.info
                    else:
                        #sinon si self est un fils gauche
                        if parent.fg is self:
                            parent.fg = predec                        
                        else:
                            parent.fd = predec
                        #le  plus proche prédécesseur hérite des fils de self
                        predec.fg = self.fg
                        predec.fd = self.fd                  
                else:
                    #remplacement par le plus proche successeur
                    (succ, parentsucc) = self.plusPetitSuccesseur()
                    #si le plus proche successeur a un fils droit
                    #on détache le  plus proche successeur
                    if parentsucc.fg is succ:
                        parentsucc.fg = succ.fd                        
                    else:
                        parentsucc.fd = succ.fd
                    #on insère le  plus proche successeur à la place du noeud
                    #cas où self est le noeud racine
                    if parent is None:
                        self.info =succ.info
                    else:
                        #si self est un fils gauche
                        if parent.fg is self:
                            parent.fg = succ                        
                        else:
                            parent.fd = succ
                        #le  plus proche successeur hérite des fils de self
                        succ.fg = self.fg
                        succ.fd = self.fd
                        #on libère le noeud        
                    
        #sinon si e < self.info on cherche à le supprimer dans le fils gauche            
        elif e < self.info:
            self.fg.supprimerElement(e, self)
        #sinon on cherche à le supprimer dans le fils droit
        elif e > self.info:
            self.fd.supprimerElement(e, self)           
            
            
            


# In[19]:


B = ABR(2)
B.insererElement(1)
B.insererElement(4)
A = ABR(3)
A.fg = B
A.fd = ABR(5)
A.affichage()
A.estABR()


# In[9]:


##Tests

arbre = ABR()
for k in [5,2,3,1,7,8]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre.insererElement(k)
    print("Affichage parcours infixe")
    arbre.afficherParcoursInfixe()
    print("Affichage parcours préfixe")
    arbre.afficherParcoursPrefixe()
    print("Affichage parcours préfixe itératif")
    arbre.parcoursPrefixeIteratif()
    print("Affichage parcours postfixe")
    arbre.afficherParcoursPostfixe()
    print("Affichage parcours en largeur")
    arbre.afficherParcoursLargeur()
print("Hauteur : ", arbre.hauteur())
arbre.affichage()
arbre.afficherArbre()
print()
print("Recherche d'élément")
for k in [5,2,3,1,7,8, 9]:
    print(f"{k} dans arbre : ", arbre.rechercheElement(k))
print("Recherche itérative d'élément")
for k in [5,2,3,1,7,8, 9]:
    print(f"{k} dans arbre : ", arbre.rechercheIterativeElement(k))
print("Test de plus grand prédécesseur ")
for k in [5,2,3,1,7,8]:
    noeud = arbre.rechercheElement(k)[1]
    pgp = noeud.plusGrandPredecesseur()
    pgp2 = noeud.plusGrandPredecesseur2()
    print(f"{k} a pour plus grand prédécesseur (version 1) : {pgp[0].info} de père {pgp[1].info}")
    print(f"{k} a pour plus grand prédécesseur (version 2) : {pgp2[0].info} de père {pgp2[1].info}")
print("Test de plus petit successeur")
for k in [5,2,3,1,7,8]:
    noeud = arbre.rechercheElement(k)[1] 
    pps = noeud.plusPetitSuccesseur()
    pps2 = noeud.plusPetitSuccesseur2()
    print(f"{k} a pour plus petit successeur (version 1) : {pps[0].info} de père {pps[1].info}")
    print(f"{k} a pour plus petit successeur (version 2) : {pps2[0].info} de père {pps2[1].info}")
print("Recherche itérative d'élément")
for k in [5,2,3,1,7,8, 9]:
    print(f"{k} dans arbre : ", arbre.rechercheIterativeElement(k))
print("Construction d'un arbre 2 avec les mếmes valeurs insérées dans le même ordre")
arbre2 = ABR()
for k in [5,2,3,1,7,8]:
    arbre2.insererElement(k)
print(f"arbre == arbre2, {arbre == arbre2}")
print("Insertion d'une autre valeur 9 dans arbre 2")
arbre2.insererElement(9)
print(f"arbre == arbre2, {arbre == arbre2}")
print("Affichage parcours en largeur de arbre2")
arbre2.afficherParcoursLargeur()
print("Construction d'un arbre 3  avec les mếmes valeurs que dans arbre mais insérées dans le désordre")
arbre3 = ABR()
for k in reversed([5,2,3,1,7,8]):
    arbre3.insererElement(k)
print(f"arbre == arbre3, {arbre == arbre3}")
print("Affichage parcours en largeur de arbre3")
arbre3.afficherParcoursLargeur()
arbre4 = ABR()
for k in [5,3,4,1,6]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre4.insererElement(k)
arbre4.afficherParcoursPrefixe()
print("Branche maximale glouton d'arbre non optimale")
print(arbre4.brancheMaximaleGlouton())
print(arbre4.brancheMaximaleGlouton2())
print("Branche maximale dynamique d'arbre (optimale)")
print(arbre4.brancheMaximaleDynamique())
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

arbre4 = ABR()
for k in [5,3,4,1,7,6,2]:
    print('-'*20)
    print(f"Insertion de {k}")
    arbre4.insererElement(k)
arbre4.affichage()
print()
print("Branche maximale glouton d'arbre non optimale")
print(arbre4.brancheMaximaleGlouton())
print("Branche maximale dynamique d'arbre (optimale)")
print(arbre4.brancheMaximaleDynamique())

print("Suppression d'éléments")
print("Suppression d'une feuille", 2)
arbre4.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression d'un élément avec un fils", 7)
arbre4.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Réinsertion des éléments supprimés")
arbre4.insererElement(2)
arbre4.insererElement(7)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression d'un élément avec deux fils", 3)
arbre4.supprimerElement(3, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression de la racine ", 5)
arbre4.supprimerElement(5, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 2)
arbre4.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 4)
arbre4.supprimerElement(4, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 1)
arbre4.supprimerElement(1, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 7)
arbre4.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 6)
arbre4.supprimerElement(6, None)
print("Affichage parcours préfixe")
arbre4.affichage()


# In[ ]:



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
        if self.info != other.info or (self.fg and not other.fg) or (not self.fg and other.fg)                                    or (self.fd and not other.fd) or (not self.fd and other.fd) :
            return False
        if self.info is None :
            return True
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
    
    def liberer(self, parent = None):
        #suppression du fils et du lien pere/fils
        if parent.fg is self :
            parent.fg = None
        else:
            parent.fd = None
        self.info = None
        self.fd = None
        self.fg = None        
    
    def supprimerElement(self, elmt, parent = None) :
        if not self :  
            return
        # si elmt est inférieur à la valeur du self, rechercher dans le sous-arbre gauche
        if elmt < self.info and self.fg :
            self.fg.supprimerElement(elmt, self)
        # si elmt est sépérieur à la valeur du self, rechercher dans le sous-arbre droit
        elif elmt > self.info and self.fd:
            self.fd.supprimerElement(elmt, self)
        elif elmt == self.info : #On a trouvé l'élément à supprimer
            # ne pas mettre else car element peut etre pas present !!
            # si self est une feuille (n'a pas d'enfant !)
            if not self.fg and not self.fd :
                 self.liberer(parent)               
            # self a un fils unique à doite
            elif not self.fg :
                if parent.fg is self:
                    parent.fg = self.fd
                else:
                    parent.fd = self.fd
            # self a un fils unique à gauche
            elif not self.fd :
                if parent.fg is self:
                    parent.fg = self.fg
                else:
                    parent.fd = self.fg
            # self a deux fils
            else :
                # il faut remplacer la valeur de self par celle de son plus proche predecesseur/successeur ppp/pps
                 
                #on alterne pour équilibrer ???
                if randint(0, 1) == 1:
                    #remplacement par le plus proche prédécesseur
                    print('plus proche predécésseur')
                    (pred, parentpred) = self.plusGrandPredecesseur()
                    self.info = pred.info
                    #si le ppprédécesseur a un fils gauche, il ne peut pas avoir de fils droit : + gd pred !!
                    #on fait pointer le parent de pppredecesseur sur ce fils gauche, et c'est necessairement parent.fd !!
                    if pred.fg :
                        parentpred.fd  = pred.fg
                    #on libère le noeud
                    pred.liberer(parentpred)
                else :
                    #remplacement par le plus proche successeur
                    print('plus proche successeur')
                    (succ, parentsucc) = self.plusPetitSuccesseur()
                    self.info = succ.info
                    #si le pps a un fils droit, il ne peut pas avoir de fils gauche : + petit succ !!
                    #on fait pointer le parent de pps (qui est necessairement parent.fg) sur ce fils droit !!
                    if succ.fd :
                        parentsucc.fg  = succ.fd
                    #on libère le noeud
                    succ.liberer(parentsucc)

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

print('-' * 30)
print("Test suppression Brigitte")
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

print()
print('-' * 30)

print("Test suppression Fred")
print("Suppression d'éléments")
print("Suppression d'une feuille", 2)
arbre4.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression d'un élément avec un fils", 7)
arbre4.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Réinsertion des éléments supprimés")
arbre4.insererElement(2)
arbre4.insererElement(7)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression d'un élément avec deux fils", 3)
arbre4.supprimerElement(3, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression de la racine ", 5)
arbre4.supprimerElement(5, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 2)
arbre4.supprimerElement(2, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 4)
arbre4.supprimerElement(4, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 1)
arbre4.supprimerElement(1, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 7)
arbre4.supprimerElement(7, None)
print("Affichage parcours préfixe")
arbre4.affichage()
print("Suppression du noeud", 6)
arbre4.supprimerElement(6, None)
print("Affichage parcours préfixe")
arbre4.affichage()

