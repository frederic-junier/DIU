""" A Python Class for Non Oriented Graphes
LG nov 2016 and Feb 2020 
adapted from http://www.python-course.eu/Graphes_python.php
"""
from copy import deepcopy
# for dot output
from graphviz import Digraph
#from collections import defaultdict

class Error(Exception):
    """Classe de base pour les exceptions dans ce module."""
    pass  

class GrapheError(Error):
    """Exception levée pour les boucles auto."""
    def __init__(self, message):
        self.message = message
        

class Graphe(object):
    def __init__(self, grapheDict=None):    
        """initialise un objet Graphique
        Si aucun dictionnaire n'est fourni, un dictionnaire vide sera utilisé"""
        if grapheDict is None:
        #portée des variables... Evite que cette valeur par défaut soit partagée entre des appels successifs...
            grapheDict = {}
        self.__grapheDict = grapheDict

    def listeSommets(self):
        """renvoie la liste ordonnée des sommets d'un graphe"""
        L = list(self.__grapheDict.keys())
        if L[0][0] in '123456789' :     #pour oronner selon que sommets sont des lettres ou chiffres...
            L = [int(k) for k in L]
        L.sort()
        L = [str(k) for k in L]
        return L

    def __genereAretes(self):
        """méthode statique qui renvoie la liste de l'ensemble des arêtes
        (attention : ne pas les prendre deux fois)."""
        aretes = []
        for sommet in self.__grapheDict:
            for voisin in self.__grapheDict[sommet]:
                if {voisin, sommet} not in aretes:
                    aretes.append({sommet, voisin})
        return aretes

    def listeAretes(self):
        """renvoie les aretes d'un graphe"""
        return self.__genereAretes()

    def listeVoisins(self, sommet):
        """renvoie la liste orientée des voisins"""
        L = self.__grapheDict[sommet]
        if L !=[] :
            if L[0][0] in '123456789' :
                L = [int(k) for k in L]
            L.sort()
            L = [str(k) for k in L]
        return L

    def ajouterSommet(self, sommet):
        """Si sommet n'est pas déjà dans self, on ajoute une clé au dictionnaire GrapheDict,
        avec une liste vide comme une valeur. Sinon, rien ne doit être fait."""
        if sommet not in self.__grapheDict:
            self.__grapheDict[sommet] = []

    def ajouterArete(self, arete):
        """l'arete doit être une paire de sommets distincts et non (c, c)"""
        try :
            (sommet1, sommet2) = arete
            if sommet1 == sommet2 :
                raise GrapheError("Pas de boucle sur elle-même !")
            if sommet1 in self.__grapheDict :
                self.__grapheDict[sommet1].append(sommet2)
            else :
                self.__grapheDict[sommet1] = [sommet2]
            if sommet2 in self.__grapheDict :
                self.__grapheDict[sommet2].append(sommet1)
            else :
                self.__grapheDict[sommet2] = [sommet1]
        except GrapheError as s :
            print("Problème avec l'ajout : "+s.message)
            pass

    def __str__(self):
        res = "ListeSommets: "
        for k in self.__grapheDict:
            res += str(k) + " "
        res += "\naretes: "
        for arete in self.__genereAretes():
            res += str(arete) + " "
        return res

    def supprimerSommet(self, sommet):
        '''suppime le sommet dans self et toutes les aretes adjacentes'''
        dico = self.__grapheDict
        for voisin in dico[sommet] :
            dico[voisin].remove(sommet)
        del dico[sommet]

    def supprimerArete(self, arete):
        (sommet1, sommet2) = arete
        self.__grapheDict[sommet1].remove(sommet2)
        self.__grapheDict[sommet2].remove(sommet1)

    def parcoursDFS(self, sommetDebut):
        '''parcours en profondeur (ou DFS, pour Depth First Search en anglais)'''
        vus = []
        pile = [sommetDebut]
        while pile != [] :
            sommet = pile.pop()
            if sommet not in vus :
                vus.append(sommet)
                voisins = self.listeVoisins(sommet)
                voisins.reverse()
                for voisin in voisins :
                    pile.append(voisin)
        return vus

#     def parcoursDFS_rec(self, vus=[],sommetDebut) : 
#         vus.append(sommetDebut)
#         for vois in self.listeVoisns(sommetDebut) :
#             if vois not in vus :
#                 return self.parcoursDFS_rec(vus,vois)
                
# sol de Fred                
#     def parcoursDFS_rec(self, sommetDebut):
#         vus = []
#         dico = self.__grapheDict
#         def aux(sommet):
#             vus.append(sommet)
#             for voisin in dico[sommet] :
#                 if voisin not in vus :
#                     aux(voisin)
#         return aux(sommetDebut)
    
    def parcoursBFS(self, sommetDebut):
        '''parcours en largeur (ou BFS, pour Breadth First Search en anglais)'''
        vus = []
        file = [sommetDebut]
        while file != [] :
            sommet = file.pop(0)
            if sommet not in vus :
                vus.append(sommet)
                for voisin in self.listeVoisins(sommet) :
                    file.append(voisin)
        return vus

    def cheminEntre(self, sommet1, sommet2):
        # Could be better implemented
        return sommet2 in self.parcoursDFS(sommet1) and len(self.parcoursDFS(sommet1))!=1    

    def composantesConnexes(self):
        composantes = []
        sommets = self.listeSommets()
        while sommets != [] :
            compoConnexe = self.parcoursDFS(sommets[0])
            for sommet in compoConnexe :
                sommets.remove(sommet)
            composantes.append(compoConnexe)
        return composantes

    def contientCycle(self) : 
        pile = []
        vus = []
        sommets = list(self.__grapheDict.keys())
        while sommets :
            sommet = sommets.pop()
            pile.append(sommet)
            while pile != [] :
                sommet = pile.pop()
                for voisin in self.__grapheDict[sommet] :
                    if voisin not in vus :
                        pile.append(voisin)
                if sommet in vus :        
                    return True
                else :
                    vus.append(sommet)
        return False


    # Une heuristique de coloration non optimale basée sur la proposition de Kempe
    # Renvoie Faux si le graphe n'est pas coloriable avec cette heuristique     
    def colorier(self, K):  # color with <= K color, returns a map vertex-> color
        classement = []
        copieGraphe = deepcopy(self)
        while copieGraphe.__grapheDict :
            sommets = list(copieGraphe.__grapheDict)
            sommets.sort(key = lambda v : len(copieGraphe.__grapheDict[v]))
            pointeur = sommets[0]
            classement.append(pointeur)
            copieGraphe.supprimerSommet(pointeur)
        #print(couleurSommet)
        couleurSommets = {}
        dico = self.__grapheDict
        for v in classement :
            voisinsColores = [x for x in dico[v] if x in couleurSommets]
            couleurPossible = [i for i in range(K)
                            if not(i in [couleurSommets[v1]
                                         for v1 in voisinsColores])]
            if couleurPossible :
                couleur = min(couleurPossible)
                couleurSommets[v] = couleur
            else:
                return False
        return couleurSommets

    def print_dot(self, name='toto', colors={}):
        """Utilise Grapheviz pour imprimer le Graphe. Les couleurs sont facultatives."""
        palette = ['red','blue', 'green', 'yellow'] + (['black'] * 10)
        dot = Digraph(comment = 'My Graphe')
        for k in self.__grapheDict:
            if not colors :
                dot.node(k, k, color="red")
            else:
                dot.node(k, k, color=palette[colors[k]])
        for arete in self.__genereAretes():
            print(arete)
            (sommet1, sommet2) = list(arete)[0], list(arete)[1]
            dot.edge(sommet1, sommet2, dir="none")
        print(dot.source)
        dot.render(name, view=True)        # print in pdf  #graph.print_dot(str(time()))