#!/usr/bin/env python3

################## Imports de modules ####################

from copy import deepcopy
# for dot output
from graphviz import Digraph
import numpy as np



###############  Définitions de classes ####################


## Classes d'exceptions

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GraphError(Error):
    """Exception raised for self loops """
    def __init__(self, message):
        self.message = message


## Classe de graphe non orienté

class Graph(object):
    """Classe de graphes non orientés.
    
    >>> graph = Graph({'a' : ['d', 'z', 'b'], 'b' : ['a', 'c'], 'c':['e', 'd', 'b'], 'd':['a', 'c'], 'e' : ['z','c'], 'f' : ['g'], 'g':['f','h'], 'h':['g'], 'z' : ['a', 'e']})

    >>> graph.get_graph_dict()
    {'a': ['d', 'z', 'b'], 'b': ['a', 'c'], 'c': ['e', 'd', 'b'], 'd': ['a', 'c'], 'e': ['z', 'c'], 'f': ['g'], 'g': ['f', 'h'], 'h': ['g'], 'z': ['a', 'e']}

    >>> graph.vertices()
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'z']

    >>> graph.get_edges() == [{'d', 'a'}, {'z', 'a'}, {'b', 'a'}, {'b', 'c'}, {'c', 'e'}, {'c', 'd'}, {'z', 'e'}, {'g', 'f'}, {'g', 'h'}]
    True

    >>> graph.dfs_traversal('a')
    ['a', 'b', 'c', 'd', 'e', 'z']

    >>> graph.dfs_traversal('f')
    ['f', 'g', 'h']

    >>> graph.bfs_traversal('a')
    ['a', 'd', 'z', 'b', 'c', 'e']

    >>> graph.detect_cycle()
    True

    >>> graph.color(2)
    False

    >>> graph.color(3)
    {'f': 0, 'g': 1, 'h': 0, 'b': 0, 'a': 1, 'd': 0, 'c': 1, 'e': 0, 'z': 2}

    >>> graph.add_vertex('x')

    >>> graph.vertices() == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'z', 'x']
    True

    >>> graph.add_edge({'x', 'f'})

    >>> graph.get_edges() == [{'d', 'a'}, {'z', 'a'}, {'b', 'a'}, {'b', 'c'}, {'c', 'e'}, {'c', 'd'}, {'z', 'e'}, {'g', 'f'}, {'x', 'f'}, {'g', 'h'}]
    True
    """

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        #il est préférable de ne pas passer un objet muable
        #en paramètre
        if graph_dict is None:
            graph_dict = {}
        self.__graph_dict = graph_dict
        self.__mat_adj = None
        self.__index_vertices = None
        

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def neighbours(self, vertex):
        return self.__graph_dict[vertex]

    def get_graph_dict(self):
        """Returns private attribute __graph_dict read only"""
        return self.__graph_dict

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ edge should be a pair and not (c,c)
        """
        try:
            (vertex1, vertex2) = edge
            if vertex1 == vertex2:
                raise GraphError("no self loop")
            if vertex1 in self.__graph_dict:
                self.__graph_dict[vertex1].append(vertex2)
            else:
                self.__graph_dict[vertex1] = [vertex2]
            if vertex2 in self.__graph_dict:
                self.__graph_dict[vertex2].append(vertex1)
            else:
                self.__graph_dict[vertex2] = [vertex1]
        except GraphError as s:
            print("pb with adding edge: "+s.message)
            pass 

    def __generate_edges(self):
        """ A static method generating the set of edges
        (they appear twice in the dictionnary). Returns a list of sets.
        """
        edges = []
        for vertex in self.vertices():
            for neighbour in self.neighbours(vertex):
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def get_edges(self):
        """Return list of edges"""
        return self.__generate_edges()
        
    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


    def delete_vertex(self, vertex):  # delete vertex and all the adjacent edges
        gdict = self.__graph_dict
        for neighbour in gdict[vertex]:
            gdict[neighbour].remove(vertex)
        del gdict[vertex]

    def delete_edge(self, edge):
        (v1, v2) = edge
        self.__graph_dict[v1].remove(v2)
        self.__graph_dict[v2].remove(v1)
    
    def set_index_vertices(self):
        self.__index_vertices = {vertex : k for k, vertex in enumerate(self.vertices())}

    def get_index_vertices(self):
        if self.__index_vertices is None:
            self.set_index_vertices()
        return self.__index_vertices

    def set_mat_adj(self):
        """Construit la matrice d'adjacence du graphe.
        """
        self.set_index_vertices()
        degree = len(self.vertices())
        self.__mat_adj = np.array([ [0] * degree for _ in range(degree)])
        for vertex1 in self.vertices():
            for vertex2 in self.neighbours(vertex1):
                self.__mat_adj[self.__index_vertices[vertex1]][self.__index_vertices[vertex2]] = 1
    
    def get_mat_adj(self):
        if self.__mat_adj is None:
            self.set_mat_adj()
        return self.__mat_adj


    def dfs_traversal2(self, root, verbose = True):
        seen = {vertex : False for vertex in self.vertices()}
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement DFS : use .pop() 
        while todo:
            vertex = todo.pop()
            if verbose:
                print(vertex, end = ' , ' )    
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    todo.append(neighbour)
                    seen[neighbour] = True
        

    def dfs_traversal_rec2(self, roo, verbose = True):

        seen = {vertex : False for vertex in self.vertices()}
        gdict = self.__graph_dict

        def aux(vertex):
            seen[vertex] = True
            if verbose:
                print(vertex, end = ' , ' )
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    aux(neighbour)

        aux(root)

    def dfs_traversal(self, root):
        seen = []   #j'intialiserais avec seen = [root]
        todo = [root]
        gdict = self.__graph_dict
        #print(gdict)
        # TODO : Implement DFS : use .pop() 
        while todo:
            vertex = todo.pop()
            if vertex not in seen:
                seen.append(vertex)  
                for neighbour in gdict[vertex]:
                    if neighbour not in seen: #pas terrible en complexité
                        todo.append(neighbour)                    
        return seen

   
    def dfs_traversal_rec(self, root, verbose = True):

        seen = []
        gdict = self.__graph_dict

        def aux(vertex):
            seen.append(vertex)
            if verbose:
                print(vertex, end = ' , ' )
            for neighbour in gdict[vertex]:
                if neighbour not in seen:
                    aux(neighbour)

        return aux(root)

    def bfs_traversal(self, root):
        seen = [root]
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement BFS : use .pop(0) to dequeue
        while len(todo) > 0:
            vertex = todo.pop(0)
            for neighbour in gdict[vertex]:
                if neighbour not in seen:
                    todo.append(neighbour)
                    seen.append(neighbour)                    
        return seen


    def bfs_traversal_correction(self, root): #slide 26 du cours généralités
        seen = []     # == L
        todo = [root] # B
        gdict = self.__graph_dict
        print(gdict)
        # TODO : Implement BFS : use .pop(0) to dequeue
        while len(todo) > 0:
            current = todo.pop(0)
            seen.append(current)
            for neighbour in gdict[current]:
                if neighbour not in seen and neighbour not in todo:
                    todo.append(neighbour)                    
        return seen


    def bfs_traversal2(self, root, verbose = True):
        seen = {vertex : False for vertex in self.vertices()}
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement BFS : use .pop(0) to dequeue
        while todo:            
            vertex = todo.pop(0)
            if verbose:
                print(vertex, end = ' , ' )
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    todo.append(neighbour)
                    seen[neighbour] = True


    def is_reachable_from(self, v1, v2):
        # Could be better implemented
        return v2 in self.dfs_traversal(v1)

    def connex_components(self):
        """Retourne la liste des composantes connexes"""
        components = []
        todo = self.vertices()
        done = []
        # TODO : find CCs 
        for vertex in todo:
            if vertex not in done:
                seen = self.dfs_traversal(vertex)
                done.extend(seen)
                components.append(seen)
        return components

    def connex_components2(self):
        """Retourne la liste des composantes connexes"""
        components = []
        todo = self.vertices()
        done = {vertex : False for vertex in todo}
        # TODO : find CCs 
        for vertex in todo:
            if not done[vertex]:
                seen = self.dfs_traversal2(vertex)
                done.update(seen)
                components.append(list(seen.keys()))
        return components

    def detect_cycle2(self):
        """Détection de cycle pour graphe non orienté, version lourde.
         Au départ, tous les noeuds sont marqués comme n'ayant pas été visités. 
         Lors du parcours en profondeur, on marque comme étant "en cours de visite" 
         les noeuds pour lesquels un appel récursif est en cours 
         et comme "déjà visités"
         les noeuds pour lesquels l'appel récursif s'est terminé. 
         Si un appel récursif est fait sur un noeud qui est dans l'état "en cours de visite", 
         cela signifie que l'ensemble des noeuds en cours de visite forment un cycle, 
         donc qu'il y a un cycle dans le graphe. Si cela ne se produit jamais, 
         c'est que le graphe ne contient pas de cycle.

        Lorsque le graphe contient un cycle, on est certain de retomber 
        sur un noeud dans l'état "en cours de visite"
        au cours du parcours. En effet, lorsque l'on appelle la fonction récursive
        pour la première fois sur un noeud faisant partie d'un cycle, le parcours en profondeur
        va énumérer tous les noeuds de ce cycle, et retomber sur le premier noeud, 
        avant que l'appel ne se termine.  
        Pour un graphe non orienté on vérifie également qu'on ne revient pas au noeud parent
        ce qui reviendrait à emprunter 2 fois de suite la même arête (on aurait alors toujours un cycle)      
        """
        
        gdict = self.__graph_dict
        TRAITE = 2
        EN_COURS = 1
        PAS_VU = 0
        marque = {vertex : PAS_VU for vertex in self.vertices()}

        def search_dfs(vertex, parent = None):
            marque[vertex] = EN_COURS
            rep = False
            for neighbour in gdict[vertex]:
                if marque[neighbour] == PAS_VU:
                    marque[neighbour] = EN_COURS
                    rep = rep or search_dfs(neighbour, parent = vertex)
                #pour un graphe non orienté on vérifie qu'on n'emprunte pas 2 fois de suite la même arête
                elif marque[neighbour] == EN_COURS and neighbour != parent:  
                    return True
            marque[vertex] = TRAITE
            return rep
        
        for vertex in self.vertices():
            if marque[vertex] == PAS_VU and search_dfs(vertex):
                return True
        return False

    def detect_cycle(self):
        """Détection de cycle récursive pour graphe non orienté 
        """
        
        gdict = self.__graph_dict
        VU = 1
        PAS_VU = 0
        marque = {vertex : PAS_VU for vertex in self.vertices()}

        def search_dfs(vertex, parent = None):
            marque[vertex] = VU
            rep = False
            for neighbour in gdict[vertex]:
                if marque[neighbour] == PAS_VU:
                    rep = rep or search_dfs(neighbour, parent = vertex)
                #pour un graphe non orienté on vérifie qu'on n'emprunte pas 2 fois de suite la même arête
                elif neighbour != parent:  
                    return True
            return rep
        
        for vertex in self.vertices():
            if marque[vertex] == PAS_VU and search_dfs(vertex):
                return True
        return False

    def contientCycle(self) : 
        """Détection de cycle version de Brigitte Mougeot"""
        pile = []    #sommets à traiter
        sommets = self.vertices()   #sommets non traités
        while sommets :
            vus = []          #sommets en cours de traitement
            sommet = sommets.pop()
            pile.append(sommet)
            while pile != [] : 
                print(pile, vus)               
                sommet = pile.pop()                
                for voisin in self.__graph_dict[sommet] :
                    if voisin not in vus :
                        pile.append(voisin)
                        #on ajoute voisin dans la pile des sommets à traiter
                        #si on retournait True parce que voisin dans vus ?
                        #ce serait faux si on ne vérifie pas si voisin est le parent de sommt
                        #voir version 2 ci-dessous
                #si le sommet est déjà dans vus quand on doit  le traitee
                #c'est qu'il a déjà été taité/vu avant et qu'on a un cycle
                if sommet in vus :        
                    return True
                else :
                    vus.append(sommet)
        return False


    def contientCycle2(self) : 
        """Détection de cycle version de Brigitte Mougeot adaptée"""
        pile = []        
        sommets = self.vertices()
        while sommets :
            vus = []
            sommet = sommets.pop()
            pile.append((sommet, None))
            while pile != [] :                
                sommet, parent = pile.pop()
                vus.append(sommet)
                for voisin in self.__graph_dict[sommet] :
                    if voisin not in vus:
                        pile.append((voisin,sommet))
                    #ici on a besoin de vérifier que le voisin n'est pas le parent qui est déjà dans vus
                    elif  voisin != parent:  
                        return True
               
        return False


    def coloration(self, K):
        """Coloration du graphe avec l'heuristique de Kempe
        Retourne un dictionnaire dont les clefs sont les sommets 
        et les valeurs des numéros de couleurs  à partir de 0"""
        todo_vertices = []
        gcopy = deepcopy(self)
        while gcopy.vertices():
            todo = list(gcopy.vertices())
            todo.sort(key = lambda v : len(gcopy.neighbours(v)))
            lower = todo[0]
            todo_vertices.append(lower)
            gcopy.delete_vertex(lower)
        coloring = dict()
        for vertex in todo_vertices[::-1]:
            set_indexcolor_neighbour = {coloring[neighbour] for neighbour in self.neighbours(vertex) if neighbour in coloring}
            set_index_free = set(range(K)).difference(set_indexcolor_neighbour)
            if set_index_free:
                coloring[vertex] = min(set_index_free)
            else:
                return False  
        return coloring
            

    # One non optimal coloring heuristic based on Kempe's proposition
    # returns False if the graph is not colorable with this heuristic
    def color(self, K):  # returns a map vertex-> color
        todo_vertices = []
        gcopy = deepcopy(self)
        while gcopy.__graph_dict:
            todo = list(gcopy.__graph_dict)
            todo.sort(key=lambda v: len(gcopy.__graph_dict[v]))
            lower = todo[0]
            todo_vertices.append(lower)
            gcopy.delete_vertex(lower)
        #print(todo_vertices)
        coloring = {}
        gdict = self.__graph_dict
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

    def print_dot(self, name="toto", showgraph = False, colors={}):
        """
        Use graphviz to print the graph. Colors is optional.
        """
        foo = ['red', 'blue', 'green', 'yellow'] + (['black'] * 10)
        dot = Digraph(comment='My Graph')
        for k in self.__graph_dict:
            if not(colors):
                dot.node(k, k, color="red")
            else:
                dot.node(k, k, color=foo[colors[k]])
        for edge in self.__generate_edges():
            #print(edge)
            (v1, v2) = list(edge)[0], list(edge)[1]
            dot.edge(v1, v2, dir="none")
        #print(dot.source)
        dot.render(name, view=showgraph)        # print in pdf

    
## Classe de graphe orienté


class DirectGraph(Graph):

    """
    Classe de graphes orientés, hérite de la classe graphe, ci-dessous quelques exemples de résultats attendus pour doctest.

    >>> directgraph1 = DirectGraph(graph_dict={"1" : ["2", "4"], "2" : [], "3" : ["2", "5"], "4" : ["6"], "5" : ["4", "3"], "6" : [] })

    >>> directgraph1.get_graph_dict()
    {'1': ['2', '4'], '2': [], '3': ['2', '5'], '4': ['6'], '5': ['4', '3'], '6': []}

    >>> directgraph1.vertices()
    ['1', '2', '3', '4', '5', '6']

    >>> directgraph1.get_edges()
    [('1', '2'), ('1', '4'), ('3', '2'), ('3', '5'), ('4', '6'), ('5', '4'), ('5', '3')]


    >>> directgraph1.bfs_traversal('1')
    ['1', '2', '4', '6']

    >>> directgraph1.bfs_traversal('3')
    ['3', '2', '5', '4', '6']

    >>> directgraph1.dfs_traversal('3')
    ['3', '5', '4', '6', '2']

    >>> directgraph1.get_transitive_closure_floydWarshall()
    [[False, True, False, True, False, True], [False, False, False, False, False, False], [False, True, True, True, True, True], [False, False, False, False, False, True], [False, True, True, True, True, True], [False, False, False, False, False, False]]
    
    >>> directgraph1.get_transitive_closure()
    array([[0, 1, 0, 1, 0, 1],
           [0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0, 1],
           [0, 1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0, 0]])
           
    >>> directgraph1.add_edge(("1", "3"))
    
    >>> directgraph1.get_edges()
    [('1', '2'), ('1', '4'), ('1', '3'), ('3', '2'), ('3', '5'), ('4', '6'), ('5', '4'), ('5', '3')]
    
    >>> directgraph1.add_vertex("7")
    
    >>> directgraph1.add_edge(("7", "1"))
    
    >>> directgraph1.get_edges()
    [('1', '2'), ('1', '4'), ('1', '3'), ('3', '2'), ('3', '5'), ('4', '6'), ('5', '4'), ('5', '3'), ('7', '1')]
    
    >>> directgraph1.vertices()
    ['1', '2', '3', '4', '5', '6', '7']
    
    >>> directgraph1.delete_edge(("1","3"))
    
    >>> directgraph1.get_edges()
    [('1', '2'), ('1', '4'), ('3', '2'), ('3', '5'), ('4', '6'), ('5', '4'), ('5', '3'), ('7', '1')]
    
    >>> directgraph1.delete_vertex("7")
    
    >>> directgraph1.get_edges()
    [('1', '2'), ('1', '4'), ('3', '2'), ('3', '5'), ('4', '6'), ('5', '4'), ('5', '3')]
    
    >>> directgraph1.vertices()
    ['1', '2', '3', '4', '5', '6']

    >>> directgraph1.detect_cycle()
    True

    >>> directgraph1.topological_sort_greedy()
    Le graphe contient un cycle, pas de tri topologique !
    (False, [])

    >>> directgraph2 = DirectGraph(graph_dict={"1" : ["2", "3"], "2" : ["4", "5"], "3" : ["7", "5"], "4": ["6"], "5" : ["6"],"6" : ["10", "11"], "7" : [], "8" : ["7"], "9" : ["8"], "10" : ["11","9"], "11" : ["12"], "12":[]})

    >>> directgraph2.detect_cycle()
    False

    >>> directgraph2.topological_sort_greedy()
    (True, ['1', '3', '2', '5', '4', '6', '10', '9', '8', '7', '11', '12'])

    >>> directgraph2.topological_sort_dfs()
    (True, ['1', '3', '2', '5', '4', '6', '10', '9', '8', '7', '11', '12'])

    """

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        super(DirectGraph, self).__init__(graph_dict=graph_dict)
        self.__transitive_closure = None
        #pas propre il faudrait définir un getter dans la classe Graph pour accéder à son attribut privé  __graph_dict 
        self.__graph_dict = self.get_graph_dict()
        self.__distmin_floyd_warshall = None
        self.__mat_adj = None
        self.__index_vertices = None


    def add_edge(self, edge):      
        (vertex1, vertex2)  = edge
        if vertex1 in self.get_graph_dict():
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]
    
    def __generate_oriented_edges(self):
        """ A static method generating the tuples of edges.
        Returns a list of tuples.
        Private methode
        """
        edges = []
        for vertex in self.vertices():
            for neighbour in self.neighbours(vertex):
                if (vertex, neighbour) not in edges:
                    edges.append((vertex, neighbour))
        return edges

    def get_edges(self):
        """Return list of edges"""
        return self.__generate_oriented_edges()
    
    def __str__(self):
        res = "vertices: "
        for k in self.get_graph_dict():
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.get_edges():
            res += str(edge) + " "
        return res

    

    def delete_vertex(self, vertex):  # delete vertex and all the adjacent edges
        gdict = self.__graph_dict
        del gdict[vertex]

    def delete_edge(self, edge):
        (v1, v2) = edge
        self.__graph_dict[v1].remove(v2)

    def print_dot(self, name="toto", showgraph = False, colors={}):
        """
        Use graphviz to print the graph. Colors is optional.
        """
        foo = ['red', 'blue', 'green', 'yellow'] + (['black'] * 10)
        dot = Digraph(comment='My Graph')
        for k in self.vertices():
            if not(colors):
                dot.node(k, k, color="red")
            else:
                dot.node(k, k, color=foo[colors[k]])
        for edge in self.get_edges():
            #print(edge)
            (v1, v2) = list(edge)[0], list(edge)[1]
            dot.edge(v1, v2)
        #print(dot.source)
        dot.render(name, view=showgraph)        # print in pdf
 
#voir https://fr.wikipedia.org/wiki/Fermeture_transitive
#voir https://fr.wikipedia.org/wiki/Matrice_binaire
#voir https://adrien.poupa.fr/efrei/Th%C3%A9orie%20des%20graphes/FermetureMatrices.pdf
#voir http://www-igm.univ-mlv.fr/~perrin/Enseignement/X/X98/pc8/pc8Java/pc8Java.html
    def set_transitive_closure(self, verbose = False):
        """Complexité en O(n^4)"""
        mat = self.get_mat_adj()
        mat = mat.astype(bool)  #conversion de la matrice d'adjacence en matrice booléenne
        self.__transitive_closure = mat
        for k in range(1, len(self.__graph_dict)):
            mat = mat_boolean_product(mat, self.__transitive_closure)
            if verbose:
                print(f"Matrice d'adjacence binaire à la puissance {k + 1}")
                print(mat.astype(int))
            self.__transitive_closure = np.logical_or(self.__transitive_closure, mat)
        self.__transitive_closure = self.__transitive_closure.astype(int)

    def get_transitive_closure(self):
        if self.__transitive_closure is None:
            self.set_transitive_closure()
        return self.__transitive_closure

    def set_transitive_closure_floydWarshall(self):
        """Complexité en O(n^3)"""
        degree = len(self.__graph_dict)
        dist = [ [False] * degree  for _ in range(degree)]
        self.set_index_vertices()
        self.__index_vertices = self.get_index_vertices()
        #initialisation de la matrice de distance dist
        for vertex in self.vertices():
            for neighbour in self.neighbours(vertex):
                dist[self.__index_vertices[vertex]][self.__index_vertices[neighbour]] = True    
        for k in range(0, degree):
            for i in range(0, degree):
                for j in range(0, degree):                    
                    dist[i][j]  = dist[i][j] or  dist[i][k] and dist[k][j]
        self.__distmin_floyd_warshall = dist 
    
    def get_transitive_closure_floydWarshall(self):
        if self.__distmin_floyd_warshall is None:
            self.set_transitive_closure_floydWarshall()
        return self.__distmin_floyd_warshall

    def detect_cycle(self):
        """Détection de cycle pour graphe orienté 
         Au départ, tous les noeuds sont marqués comme n'ayant pas été visités. 
         Lors du parcours en profondeur, on marque comme étant "en cours de visite" 
         les noeuds pour lesquels un appel récursif est en cours 
         et comme "déjà visités"
         les noeuds pour lesquels l'appel récursif s'est terminé. 
         Si un appel récursif est fait sur un noeud qui est dans l'état "en cours de visite", 
         cela signifie que l'ensemble des noeuds en cours de visite forment un cycle, 
         donc qu'il y a un cycle dans le graphe. Si cela ne se produit jamais, 
         c'est que le graphe ne contient pas de cycle.

        Lorsque le graphe contient un cycle, on est certain de retomber 
        sur un noeud dans l'état "en cours de visite"
        au cours du parcours. En effet, lorsque l'on appelle la fonction récursive
        pour la première fois sur un noeud faisant partie d'un cycle, le parcours en profondeur
        va énumérer tous les noeuds de ce cycle, et retomber sur le premier noeud, 
        avant que l'appel ne se termine.  

        Référence France IOI : 
        Tourner en Rond Niveau 4 du parcours général 
        http://www.france-ioi.org/algo/task.php?idChapter=533&idTask=260
        """
        
        gdict = self.__graph_dict
        TRAITE = 2
        EN_COURS = 1
        PAS_VU = 0
        marque = {vertex : PAS_VU for vertex in self.vertices()}

        def search_dfs(vertex):
            marque[vertex] = EN_COURS
            rep = False
            for neighbour in gdict[vertex]:
                if marque[neighbour] == PAS_VU:
                    marque[neighbour] = EN_COURS
                    rep = rep or search_dfs(neighbour)
                elif marque[neighbour] == EN_COURS:
                    return True
            marque[vertex] = TRAITE
            return rep
        
        #boucle sur les composantes connexes
        for vertex in self.vertices():
            if marque[vertex] == PAS_VU and search_dfs(vertex):
                return True
        return False
    
    def topological_sort_greedy(self):    
        """Retourne un couple (booléen, liste) :
        le booléen indique si un ordre topologique existe
        la liste est celle des sommets dugraphe orienté triés dans un ordre topologique
        Traite d'abord les sommets de degré entrant nul et les insère dans une liste order
        dans  un ordre topologique

        Référence :
        Images des mathématiques : https://interstices.info/saider-des-graphes-pour-elaborer-une-notice-de-montage/
        """
        # on vérifie d'abord qu'il n'y ait pas de cycle
        if self.detect_cycle():
            print("Le graphe contient un cycle, pas de tri topologique !")
            return (False, [])
        #initialisation du dictionnaire des degrés entrants par sommet
        in_degree = { vertex : 0 for vertex in self.vertices() }    
        #pour chaque sommet    
        for vertex in self.vertices():
            #on compte (vertex, neighbour) pour  incrémenter le compteur de degré d'arcs entrants de 1            
            for neighbour in self.neighbours(vertex):
                in_degree[neighbour] += 1
        #start_list est la liste des sommets qui ont un degré entrant nul
        start_list = [vertex for vertex in in_degree if in_degree[vertex] == 0]
        #liste des sommets dans l'ordre tolologique
        order = []
        #tant qu'il reste des sommets non classés
        while len(start_list) != 0:
            #on récupère un sommet de degré entrant nul
            start = start_list.pop()
            #on l'ajoute à la liste des sommets dans l'ordre topologique
            order.append(start)
            #on met à jout les compteurs de dégré entrant de voisins du sommet ordonné
            for neighbour in self.neighbours(start):
                in_degree[neighbour] -= 1
                #si on a un voisin de degré entrant nul on l'insère dans la liste start_list
                if in_degree[neighbour] == 0:
                    start_list.append(neighbour)
        return (True, order) 



    def topological_sort_dfs(self):    
        """Retourne les sommets d'un graphe orienté triés dans l'ordre topologique
        Remplit une liste des sommets dans l'ordre topologique inverse en déroulant un parcours DFS

        Référence France IOI : 
        TFermeture du labyrrinthe Niveau 4 du parcours général 
        http://www.france-ioi.org/algo/task.php?idChapter=533&idTask=261
        """

        PAS_VU = 0
        VU = 1
        order = []
        vertices = self.vertices()
        #dictionnaire de marques
        #pour un DFS simple deux suffisents VU et PAS_VU
        marque = {vertex : PAS_VU for vertex in vertices}

        def search_dfs(vertex):
            """Fonction auxilaire parcours DFS"""
            #on marque le sommet comme VU
            marque[vertex] = VU
            for neighbour in self.neighbours(vertex):
                #on lance récursivement le parcours DFS sur les voisins PAS_VU
                if marque[neighbour] == PAS_VU:                    
                    search_dfs(neighbour)
            #parcours DFS depuis sommet terminé 
            #on ajoute le sommet à la liste ordonnée dans l'ordre inverse de l'ordre topologique
            order.append(vertex)
        
        if self.detect_cycle():
            print("Le graphe contient un cycle, pas de tri topologique !")
            return (False, [])

        #boucle sur les composantes connexes
        for vertex in vertices: 
            if marque[vertex] == PAS_VU:    
                search_dfs(vertex)
        #priority dans l'ordre inverse de l'ordre topologique
        return (True, order[::-1])    


    def verif_topological_order(self, order):
        """Vérifie si order est un ordre topologique sur les sommets du graphe"""
        if order == []:
            return True
        dejavu = {vertex : False for vertex in self.vertices()}
        for vertex in order:
            dejavu[vertex] = True
            for neighbour in self.neighbours(vertex):
                if dejavu[neighbour]:
                    return False
        return True

#################### Fonctions outils ########################################

def mat_boolean_product(mat1, mat2):
    """Fonction pour faire le produit de 2 matrices binaires / booléeennes"""
    n, m, p = len(mat1), len(mat2[0]), len(mat1[0])
    mat3 = np.array([ [False] * m for _ in range(n)])
    for i in range(n):
        for j in range(m):
            for k in range(p):
                mat3[i][j]= mat3[i][j] or (mat1[i][k] and mat2[k][j])
    return mat3


if __name__ == "__main__":
    #vérification des tests dans les documentations des classes
    import doctest
    doctest.testmod(verbose=True)


