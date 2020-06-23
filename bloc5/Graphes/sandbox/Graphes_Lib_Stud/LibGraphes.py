""" A Python Class for Non Oriented Graphs
LG nov 2016 and Feb 2020 
adapted from http://www.python-course.eu/graphs_python.php
"""

from copy import deepcopy
# for dot output
from graphviz import Digraph
import numpy as np


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GraphError(Error):
    """Exception raised for self loops
    """
    def __init__(self, message):
        self.message = message


class Graph(object):

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
            seen.append(vertex)  #je ferais cette mise à jour juste après avoir ajouté un voisin dans la pile
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
        seen = []
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement BFS : use .pop(0) to dequeue
        while todo:
            vertex = todo.pop(0)
            seen.append(vertex)
            for neighbour in gdict[vertex]:
                if neighbour not in seen:
                    todo.append(neighbour)                    
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

    def contientCycle(self) : 
        """Version de Brigitte"""
        pile = []    #sommets à traiter
        sommets = self.vertices()   #sommets non traités
        while sommets :
            vus = []          #sommets en cours de traitement
            sommet = sommets.pop()
            pile.append(sommet)
            while pile != [] :                
                sommet = pile.pop()
                #si le sommet est déjà dans vus quand on doit  le traitee
                #c'est qu'il a déjà été taité/vu avant et qu'on a un cycle
                if sommet in vus :        
                    return True
                else :
                    vus.append(sommet)
                for voisin in self.__graph_dict[sommet] :
                    if voisin not in vus :
                        pile.append(voisin)
                        #on ajoute voisin dans la pile des sommets à traiter
                        #si on retournait True parce que voisin dans vus ?
                        #ce serait faux si on ne vérifie pas si voisin est le parent de sommt
                        #voir version 2 ci-dessous
        return False


    def contientCycle2(self) : 
        """Version de Brigitte2"""
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

    def coloration(self, K):
        todo_vertices = []
        gcopy = deepcopy(self)
        while gcopy.vertices():
            todo = list(gcopy.vertices())
            todo.sort(key = lambda v : len(gcopy.neighbours(v)))
            lower = todo[0]
            todo_vertices.append(lower)
            gcopy.delete_vertex(lower)
        print(todo_vertices)
        coloring = dict()
        indexcolor = 0
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
    def color(self, K):  # color with <= K color, returns a map vertex-> color
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

    def print_dot(self, name="toto", colors={}):
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
            print(edge)
            (v1, v2) = list(edge)[0], list(edge)[1]
            dot.edge(v1, v2, dir="none")
        print(dot.source)
        dot.render(name, view=True)        # print in pdf

    
    



class DirectGraph(Graph):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        super(DirectGraph, self).__init__(graph_dict=graph_dict)
        self.__transitive_closure = None
        self.__graph_dict = self._Graph__graph_dict 
        self.__distmin_floyd_warshall = None
        self.__mat_adj = None
        self.__index_vertices = None


    def add_edge(self, edge):        
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]
        

    def __generate_edges(self):
        """ A static method generating the set of edges
        (they appear twice in the dictionnary). Returns a list of sets.
        """
        edges = []
        for vertex in self.vertices():
            for neighbour in self.neighbours(vertex):
                if (vertex, neighbour) not in edges:
                    edges.append((vertex, neighbour))
        return edges

    def delete_vertex(self, vertex):  # delete vertex and all the adjacent edges
        gdict = self.__graph_dict
        del gdict[vertex]

    def delete_edge(self, edge):
        (v1, v2) = edge
        self.__graph_dict[v1].remove(v2)

    def print_dot(self, name="toto", colors={}):
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
        for edge in self.__generate_edges():
            print(edge)
            (v1, v2) = list(edge)[0], list(edge)[1]
            dot.edge(v1, v2)
        print(dot.source)
        dot.render(name, view=True)        # print in pdf
 
#voir https://fr.wikipedia.org/wiki/Fermeture_transitive
#voir https://fr.wikipedia.org/wiki/Matrice_binaire
#voir https://adrien.poupa.fr/efrei/Th%C3%A9orie%20des%20graphes/FermetureMatrices.pdf
#voir http://www-igm.univ-mlv.fr/~perrin/Enseignement/X/X98/pc8/pc8Java/pc8Java.html
    def set_transitive_closure(self):
        """Complexité en O(n^4)"""
        mat = self.get_mat_adj()
        mat = mat.astype(bool)  #conversion de la matrice d'adjacence en matrice booléenne
        self.__transitive_closure = mat
        for k in range(1, len(self.__graph_dict)):
            mat = mat_boolean_product(mat, self.__transitive_closure)
            print(f"Matrice d'adjacence binaire à la puissance {k + 1}")
            print(mat.astype(int))
            self.__transitive_closure = np.logical_or(self.__transitive_closure, mat)
        print("Matrice de fermeture transitive du graphe")
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
        print(dist)
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
        
        for vertex in self.vertices():
            if marque[vertex] == PAS_VU and search_dfs(vertex):
                return True
        return False
    
    def topological_sort(self):    
        """Retourne les sommets d'un graphe orienté triés dans l'ordre topologique
        """

        PAS_VU = 0
        VU = 1
        priority = []
        vertices = self.vertices()
        root = vertices[0]
        marque = {vertex : PAS_VU for vertex in vertices}

        def search_dfs(vertex):
            marque[vertex] = VU
            for neighbour in self.neighbours(vertex):
                if marque[neighbour] == PAS_VU:                    
                    search_dfs(neighbour)
            priority.append(vertex)
        
        if self.detect_cycle():
            print("Le graphe contient un cycle, pas de tri topologique !")
            return (False, [])
        for vertex in vertices: 
            if marque[vertex] == PAS_VU:    
                search_dfs(vertex)
        #priority dans l'ordre inverse de l'ordre topologique
        return (True, priority[::-1])    


def mat_boolean_product(mat1, mat2):
    """Fonction pour faire le produit de 2 matrices binaires / booléeennes"""
    n, m, p = len(mat1), len(mat2[0]), len(mat1[0])
    mat3 = np.array([ [False] * m for _ in range(n)])
    for i in range(n):
        for j in range(m):
            for k in range(p):
                mat3[i][j]= mat3[i][j] or (mat1[i][k] and mat2[k][j])
    return mat3




