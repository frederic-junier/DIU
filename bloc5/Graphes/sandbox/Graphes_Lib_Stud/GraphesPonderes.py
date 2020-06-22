""" 
A python class for *non oriented* weighted graphs
L. Gonnord nov 2016. Last modified : May 2020.
"""

from LibGraphes import Graph
# for dot output
from graphviz import Digraph

debug = False


def minimum_distance(dist, Q):
    ''' Auxiliary function for Dijkstra
    returns the minimal distance from the distinguished vertex (implicit)
    to a node in the Q set
    '''
    if debug : 
        print(Q, dist)
    return min([(dist[node], node)
                for node in Q if node is not None])[1]


class WeightedGraph(Graph):

    def __init__(self, graph_dict=None, weight_dict=None):
        ''' Constructor of weighted graphs,
        derive from its mother'''
        super(WeightedGraph, self).__init__(graph_dict)
        if weight_dict is None:
            weight_dict = {}
        self.__weight_dict = weight_dict
        self.__graph_dict = self._Graph__graph_dict 
        self.__reverse_index_vertices = None
        self.__index_vertices = None
        self.__distmin_floyd_warshall = None
       


    def my_weight(self, v1, v2):
        ''' Gives the weight of a given edge'''
        if (v1,v2) in self.__weight_dict:
            return self.__weight_dict[(v1,v2)]
        else:
            return self.__weight_dict[(v2,v1)]
            
    #true iff all edges have a weight
    def verify_weights(self):
        #        print self.__weight_dict
        for edge in self.edges():
            (v1, v2) = list(edge)[0], list(edge)[1]
            if (v1, v2) not in self.__weight_dict and (v2, v1) not in self.__weight_dict:
                return False
        return True

    def do_dijkstra(self, source):
        ''' Minimal distance from the source, for all nodes'''
        vertices = self.vertices()
        edges = self.edges()
        dist = dict()
        previous = dict()
        # Gives a special value "inf" which is not of type int, shame!
        for vertex in vertices:
            dist[vertex] = float("inf")
            previous[vertex] = None

        dist[source] = 0
        Q = set(vertices)
        # TODO : implement Dijkstra !
        while len(Q) > 0:
           vertex = minimum_distance(dist, Q)
           Q.remove(vertex)
           for  neighbour in self.neighbours(vertex):
               dn = dist[vertex] +  self.my_weight(vertex, neighbour)
               if dn < dist[neighbour]:
                   dist[neighbour] = dn
                   previous[neighbour] = vertex
        return (previous, dist)

    def print_dot_weight(self, name="toto", colors={}):
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
            for edge in self.edges():
                print(edge)
                (v1, v2) = list(edge)[0], list(edge)[1]
                #poids
                w = self.my_weight(v1, v2)
                dot.edge(v1, v2, label= str(w)   ,dir="none")
            print(dot.source)
            dot.render(name, view=True)        # print in pdf
    
    def set_reverse_index_vertices(self):
        self.set_index_vertices()
        self.__index_vertices = self.get_index_vertices()
        self.__reverse_index_vertices = {index : vertex for (vertex, index) in self.__index_vertices.items()}
    
    def get_reverse_index_vertices(self):
        if self.__reverse_index_vertices is None:
            self.set_reverse_index_vertices()
        return self.__reverse_index_vertices

    def set_FloydWarshall(self):
        degree = len(self.__graph_dict)
        dist = [ [float('inf')] * degree  for _ in range(degree)]
        self.set_index_vertices()
        self.__index_vertices = self.get_index_vertices()
        #initialisation de la matrice de distance dist
        for vertex in self.vertices():
            for neighbour in self.neighbours(vertex):
                dist[self.__index_vertices[vertex]][self.__index_vertices[neighbour]] = self.my_weight(vertex, neighbour)
        for k in range(degree):
            dist[k][k] = 0
        print(dist)
        for k in range(0, degree):
            for i in range(0, degree):
                for j in range(0, degree):                    
                    dist[i][j]  = min(dist[i][j], dist[i][k] + dist[k][j]) 
        self.__distmin_floyd_warshall = dist 
        #détection de cycle négatif
        for k in range(0, degree):
            if dist[k][k] < 0:
                return True
        return False
    
    def get_FloydWarshall(self):
        if self.__distmin_floyd_warshall is None:
            self.set_FloydWarshall()
        return self.__distmin_floyd_warshall


    def 