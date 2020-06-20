""" A Python Class for Non Oriented Graphes
LG nov 2016 and Feb 2020 
adapted from http://www.python-course.eu/Graphes_python.php
"""
from copy import deepcopy
# for dot output
from graphviz import Digraph

class Error(Exception):
    """Classe de base pour les exceptions dans ce module."""
    pass  

class GrapheError(Error):
    """Exception levée pour les boucles auto."""
    def __init__(self, message):
        self.message = message
        

class Graphe(object):
    def __init__(self, grapheDict={}):
        """initialise un objet Graphique
        Si aucun dictionnaire n'est fourni, un dictionnaire vide sera utilisé"""
        self.grapheDict = grapheDict

    def listeSommets(self):
        """renvoie la liste des sommets d'un graphe"""
        return list(self.grapheDict.keys())

    def genereAretes(self):
        """méthode statique qui renvoie la liste de l'ensemble des arêtes
        (attention : ne pas les prendre deux fois)."""
        aretes = []
        for sommet in self.grapheDict:
            for voisin in self.grapheDict[sommet]:
                if {voisin, sommet} not in aretes:
                    aretes.append({sommet, voisin})
        return aretes

    def listeAretes(self):
        """renvoie les aretes d'un graphe"""
        return self.genereAretes()

    def listeVoisins(self, sommet):
        return self.grapheDict[sommet]

    def ajouterSommet(self, sommet):
        """Si sommet n'est pas déjà dans self, on ajoute une clé au dictionnaire GrapheDict,
        avec une liste vide comme une valeur. Sinon, rien ne doit être fait."""
        if sommet not in self.grapheDict:
            self.grapheDict[sommet] = []

    def ajouterArete(self, arete):
        """l'arete doit être une paire de sommets distincts et non (c, c)"""
        try :
            (sommet1, sommet2) = arete
            if sommet1 == sommet2 :
                raise GrapheError("Pas de boucle sur elle-même !")
            if sommet1 in self.grapheDict :
                self.grapheDict[sommet1].append(sommet2)
            else :
                self.grapheDict[sommet1] = [sommet2]
            if sommet2 in self.grapheDict :
                self.grapheDict[sommet2].append(sommet1)
            else :
                self.grapheDict[sommet2] = [sommet1]
        except GrapheError as s :
            print("Problème avec l'ajout : "+s.message)
            pass

    def __str__(self):
        res = "ListeSommets: "
        for k in self.grapheDict:
            res += str(k) + " "
        res += "\naretes: "
        for arete in self.genereAretes():
            res += str(arete) + " "
        return res

    def supprimerSommet(self, sommet):
        '''suppime le sommet dans self et toutes les aretes adjacentes'''
        dico = self.grapheDict
        for voisin in dico[sommet] :
            dico[voisin].remove(sommet)
        del dico[sommet]

    def supprimerArete(self, arete):
        (sommet1, sommet2) = arete
        self.grapheDict[sommet1].remove(sommet2)
        self.grapheDict[sommet2].remove(sommet1)

    def parcoursDFS(self, sommetDebut):
        '''parcours en profondeur (ou DFS, pour Depth First Search en anglais)'''
        vus = []
        pile = [sommetDebut]
        dico = self.grapheDict
        while pile != [] :
            sommet = pile.pop()
            if sommet not in vus :
                vus.append(sommet)
                for voisin in dico[sommet] :
                    pile.append(voisin)
        return vus

    def parcoursBFS(self, sommetDebut):
        '''parcours en largeur (ou BFS, pour Breadth First Search en anglais)'''
        vus = []
        file = [sommetDebut]
        dico = self.grapheDict
        while file != [] :
            sommet = file.pop(0)
            if sommet not in vus :
                vus.append(sommet)
                for voisin in dico[sommet] :
                    file.append(voisin)
        return vus

    def cheminEntre(self, sommet1, sommet2):
        # Could be better implemented
        return sommet2 in self.parcoursDFS(sommet1)

    def composantesConnexes(self):
        composantes = []
        todo = self.listeSommets()
        while todo != [] :
            compoConnexe = self.parcoursDFS(todo[0])
            for sommet in compoConnexe :
                todo.remove(sommet)
            composantes.append(compoConnexe)
        return composantes

    # Une heuristique de coloration non optimale basée sur la proposition de Kempe
    # Renvoie Faux si le graphe n'est pas coloriable avec cette heuristique
    def colorier(self, K):  # colorie avec <= K couleurs, renvoie un dictionnaire sommet--->couleur
        couleurSommet = {}
        dico = self.grapheDict
        sommetsTries = list(dico.keys())
        sommetsTries.sort(key = lambda x : len(dico[x]))
        for sommet in sommetsTries :
            couleurInterdite = set()
            for voisin in dico[sommet] :
                if voisin in couleurSommet :
                    couleurInterdite.add(couleurSommet[voisin])
            if len(couleurInterdite) < K :
                couleurSommet[sommet] = min(k for k in range(K) if k not in couleurInterdite)
            else :
                return False
        return couleurSommet
       
    def color(self, K):  # color with <= K color, returns a map vertex-> color
        todo_vertices = []
        gcopy = deepcopy(self)
        while gcopy.grapheDict :
            todo = list(gcopy.grapheDict)
            todo.sort(key=lambda v: len(gcopy.grapheDict[v]))
            lower = todo[0]
            todo_vertices.append(lower)
            gcopy.supprimerSommet(lower)
        #print(todo_vertices)
        coloring = {}
        gdict = self.grapheDict
        for v in todo_vertices:
            seen_neighbours = [x for x in gdict[v] if x in coloring]
            choose_among = [i for i in range(K)
                            if not(i in [coloring[v1]
                                         for v1 in seen_neighbours])]
            if choose_among:
                color = min(choose_among)
                coloring[v] = color
            else:
                return False
        return coloring

    def print_dot(self, name='toto', colors={}):
        """Utilise Grapheviz pour imprimer le Graphe. Les couleurs sont facultatives."""
        palette = ['red','blue', 'green', 'yellow'] + (['black'] * 10)
        dot = Digraph(comment = 'My Graphe')
        for k in self.grapheDict:
            if not colors :
                dot.node(k, k, color="red")
            else:
                dot.node(k, k, color=palette[colors[k]])
        for arete in self.genereAretes():
            print(arete)
            (sommet1, sommet2) = list(arete)[0], list(arete)[1]
            dot.edge(sommet1, sommet2, dir="none")
        print(dot.source)
        dot.render(name, view=True)        # print in pdf
