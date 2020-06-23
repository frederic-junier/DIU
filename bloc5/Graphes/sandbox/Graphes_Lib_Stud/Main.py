# Main File to test the Graph Class
# L & S Gonnord, 2016
from LibGraphes import *

def main():
    g = { "a" : ["d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"],
          "f" : []
    }
    g2 = { "r3" : ["r1", "r2"],
           "r2" : ["r3", "r1", "c", "a"],
           "r1" : ["r3", "r2", "c"],
           "c"  : ["r1", "r2", "b", "a", "d", "e"],
           "b"  : ["a", "c", "d", "e"],
           "e"  : ["b", "c", "d"],
           "a"  : ["b", "c", "d", "r2"],
           "d"  : ["a", "b", "c", "e"]
    }
    #two graphs
    graph = Graph(g)
    graph2 = Graph(g2)
        
    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print("Matrice d'adjacence")
    print(graph.get_mat_adj())

    print("Index des sommets dans la matrice d'adjacence")
    print(graph.get_index_vertices())

    print("Add vertex:")
    graph.add_vertex("z")
    
    print("Vertices of graph:")
    print(graph.vertices())

    print("Add an edge (a, z):")
    graph.add_edge(("a","z"))
    print("Add an edge (a, a):")
    graph.add_edge(("a","a"))
    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print('Adding an edge {"x","y"} with new vertices:')
    graph.add_edge({"x","y"})
    print("Graph dict" , graph._Graph__graph_dict)
    print("Vertices of graph:")
    print(graph.vertices())
    print("Edges of graph:")
    print(graph.edges())
    print("Dfs traversal from 'a'")
    print(graph.dfs_traversal.__name__, graph.dfs_traversal('a')) #['a', 'z', 'd', 'c', 'e', 'b']
    print(graph.dfs_traversal2.__name__, graph.dfs_traversal2('a'))
    print(graph.dfs_traversal_rec.__name__, graph.dfs_traversal2('a'))
    print(graph.dfs_traversal_rec2.__name__, graph.dfs_traversal2('a'))
    print("Dfs traversal from 'd'")
    print(graph.dfs_traversal('d')) #['d', 'c', 'e', 'b', 'a', 'z']
    print(graph.dfs_traversal2.__name__, graph.dfs_traversal2('d'))
    print(graph.dfs_traversal_rec.__name__, graph.dfs_traversal2('d'))
    print(graph.dfs_traversal_rec2.__name__, graph.dfs_traversal2('d'))
    print("bfs traversal from 'd'")
    print(graph.bfs_traversal.__name__, graph.bfs_traversal('d')) #['d', 'a', 'c', 'z', 'b', 'e']
    print(graph.bfs_traversal2.__name__, graph.bfs_traversal2('d')) #['d', 'a', 'c', 'z', 'b', 'e']
    print(graph.bfs_traversal_correction.__name__, graph.bfs_traversal_correction('d')) #['d', 'a', 'c', 'z', 'b', 'e']
    print("Composantes connexes")
    print(graph.connex_components())
    print("Coloration Laure Gonnord, générer graphe avec graphviz")
    coloring = graph.color(3)
    print(coloring)
    graph.print_dot("graph1-coloration-LG", colors = coloring)
    print("Coloration Frédéric Junier, générer graphe avec graphviz")
    coloring = graph.coloration(3)
    print(coloring)
    graph.print_dot("graph1-coloration-FJ", colors = coloring)

    

    print("Delete vertex 'c'")
    graph.delete_vertex('c')

    print("Vertices of graph:")
    print(graph.vertices())
    print("Edges of graph:")
    print(graph.edges())
    print("Dfs traversal from 'a'")
    print(graph.dfs_traversal('a')) #['a', 'z', 'd', 'c', 'e', 'b']
    print("Dfs traversal from 'd'")
    print(graph.dfs_traversal('d')) #['d', 'c', 'e', 'b', 'a', 'z']
    print("bfs traversal from 'd'")
    print(graph.bfs_traversal('d')) #['d', 'a', 'c', 'z', 'b', 'e']
    print("Composantes connexes")
    print(graph.connex_components())
    print("Générer graphe avec graphviz")
    graph.print_dot("graph2")
    graph.color(0)   #False
    graph.color(3)    #{'a': 1, 'c': 1, 'b': 0, 'e': 0, 'd': 0, 'f': 0, 'y': 0, 'x': 1, 'z': 0}
 
    print("Détection de cycle dans un graphe non orienté avec cycle")
    graph2 = Graph(graph_dict={"1" : ["2", "3"], "2" : ["1"], "3" : ["1", "4", "5"], "4": ["3", "6"], "5" : ["3", "6"],
                                             "6" : ["4", "5"]})
    print("Détection de cycle 1 :",graph2.detect_cycle(),"Détection de cycle 2 :",graph2.detect_cycle2(), 
    "Détection de Brigitte 1 :",graph2.contientCycle(), "Détection de Brigitte 2 :",graph2.contientCycle2() )
    print("Affichage du graphe non orienté  avec cycle")
    graph2.print_dot("graph2")
    

    print("Détection de cycle dans un graphe non orienté  sans cycle")
    graph3 = Graph(graph_dict={"1" : ["2", "3"], "2" : ["1"], "3" : ["1", "4", "5"], "4": ["3"], "5" : ["3", "6"],
                                             "6" : [ "5"]})
    print("Détection de cycle :",graph3.detect_cycle(),"Détection de cycle 2 :",graph3.detect_cycle2(), 
    "Détection de Brigitte :",graph3.contientCycle(), "Détection de Brigitte 2 :",graph3.contientCycle2() )
    print("Affichage du  graphe  orienté avec cycle")
    graph3.print_dot("graph3")
    
    print("Détection de cycle dans un graphe non orienté  sans cycle")
    graph3 = Graph(graph_dict={"1" : ["2", "3"], "2" : ["1"], "3" : ["1", "4", "5"], "4": ["3"], "5" : ["3", "6"],
                                             "6" : [ "5"]})
    print("Détection de Brigitte :",graph3.contientCycle() )
    print("Affichage du  graphe  orienté avec cycle")
    graph3.print_dot("graph3")

    

    
    print("Test de graphe orienté")
    directgraph = DirectGraph(graph_dict={"1" : ["2", "4"], "2" : [], "3" : ["2", "5"],
                            "4" : ["6"], "5" : ["4", "3"], "6" : [] })
    print("Affichage du graphe")
    directgraph.print_dot("directgraph")
    print(directgraph)
    print("Index des sommets dans la matrice d'adjacence")
    print(directgraph.get_index_vertices())
    print("Matrice d'adjacence ")
    print(directgraph.get_mat_adj())
    print("Cloture transitive du graphe avec l'algorithme naif en O(n^4)")   
    print(directgraph.get_transitive_closure())
    print("Cloture transitive du graphe avec l'algorithme de Floyd-Warshall en O(n^3)")   
    print(directgraph.get_transitive_closure_floydWarshall())



    print("Détection de cycle dans un graphe orienté sans cycle")
    directgraph2 = DirectGraph(graph_dict={"1" : ["2", "3"], "2" : ["4", "5"], "3" : ["7", "5"], "4": ["6"], "5" : ["6"],
                                             "6" : ["10", "11"], "7" : [], "8" : ["7"], "9" : ["8"], "10" : ["11","9"], "11" : ["12"], "12":[]})
    print("Détection de cycle :",directgraph2.detect_cycle())
    print("Affichage du graphe orienté  sans cyle")
    directgraph2.print_dot("directgraph2")
    

    print("Détection de cycle dans un graphe orienté  avec cycle")
    directgraph3 = DirectGraph(graph_dict={"1" : ["2", "3"], "2" : ["4", "5"], "3" : ["5"], "4": ["6"], "5" : ["6"],
                                             "6" : ["10", "11"], "7" : ["3"], "8" : ["7"], "9" : ["8"], "10" : ["11","9"], "11" : ["12"], "12":[]})
    print("Détection de cycle :",directgraph3.detect_cycle())
    print("Affichage du  graphe  orienté avec cyle")
    directgraph3.print_dot("directgraph3")

    print("Tri topologique de directgraph ")
    print(directgraph.topological_sort())

    print("Tri topologique de directgraph2 ")
    print(directgraph2.topological_sort())

    print("Tri topologique de directgraph3 ")
    print(directgraph3.topological_sort())
    

    


    
if __name__ == '__main__':
    main()
