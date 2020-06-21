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
    print(graph.dfs_traversal('a')) #['a', 'z', 'd', 'c', 'e', 'b']
    print("Dfs traversal from 'd'")
    print(graph.dfs_traversal('d')) #['d', 'c', 'e', 'b', 'a', 'z']
    print("bfs traversal from 'd'")
    print(graph.bfs_traversal('d')) #['d', 'a', 'c', 'z', 'b', 'e']
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
    print("Cloture transitive du graphe")   
    print(directgraph.get_transitive_closure())
    
if __name__ == '__main__':
    main()
