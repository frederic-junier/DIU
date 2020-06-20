""" A Python Class for Non Oriented Graphs
LG nov 2016 and Feb 2020 
adapted from http://www.python-course.eu/graphs_python.php
"""

from copy import deepcopy
# for dot output
from graphviz import Digraph


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
        if graph_dict is None:
            graph_dict = {}
        self.__graph_dict = graph_dict

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
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.generate_edges():
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

    def dfs_traversal2(self, root):
        seen = {vertex : False for vertex in self.vertices()}
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement DFS : use .pop() 
        while todo:
            vertex = todo.pop()
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    todo.append(neighbour)
                    seen[neighbour] = True
        return seen

    def dfs_traversal_rec2(self, root):

        seen = {vertex : False for vertex in self.vertices()}
        gdict = self.__graph_dict

        def aux(vertex):
            seen[vertex] = True
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    aux(neighbour)

        return aux(root)

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

    
    def dfs_traversal_rec(self, root):

        seen = []
        gdict = self.__graph_dict

        def aux(vertex):
            seen.append(vertex)
            for neighbour in gdict[vertex]:
                if neighbour not in seen:
                    aux(neighbour)

        return aux(root)

    def bfs_traversal(self, root):
        seen = []
        todo = [root]
        gdict = self.__graph_dict
        print(gdict)
        # TODO : Implement BFS : use .pop(0) to dequeue
        while todo:
            vertex = todo.pop(0)
            seen.append(vertex)
            for neighbour in gdict[vertex]:
                if neighbour not in seen:
                    todo.append(neighbour)                    
        return seen

    def bfs_traversal2(self, root):
        seen = {vertex : False for vertex in self.vertices()}
        todo = [root]
        gdict = self.__graph_dict
        # TODO : Implement BFS : use .pop(0) to dequeue
        while todo:
            vertex = todo.pop(0)
            for neighbour in gdict[vertex]:
                if not seen[neighbour]:
                    todo.append(neighbour)
                    seen[neighbour] = True
        return seen

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
