#Main File to test the Graph Class
#LG

from GraphesPonderes import *

def main():
    g = {"a": ["b", "c", "d"],
         "b": ["a", "c", "d"],
         "c": ["a", "b", "d", "e", "f"],
         "d": ["a", "b", "c", "e"],
         "e": ["c", "d", "f"],
         "f": ["c", "e"]}

    # les poids
    w = {("a", "b"): 2, ("a", "c"): 5, ("a", "d"): 1,
         ("b", "d"): 2, ("b", "c"): 3, ("c", "d"): 3,
         ("c", "e"): 1, ("c", "f"): 5, ("d", "e"): 1, ("e", "f"): 2}

    graph = WeightedGraph(g, w)
    if not(graph.verify_weights()):
        print("attention il manque des poids")
    else:
        print("continuons")
    print("Recherche de plus court chemin à partir du sommet 'a', algorithme de Dijskstraa")
    graph.print_dot_weight("graph-dijkstraa")
    prev, dist = graph.do_dijkstra("a")
    print(dist)
    print(prev)


    print("Index des sommets")
    print(graph.get_index_vertices())
    print("Index renversé des sommets")
    print(graph.get_reverse_index_vertices())

    print("Recherche de plus court chemin toutes origines toutes destinations, algorithme de Floyd-Warshall")
    print(graph.get_FloydWarshall())

if __name__ == '__main__':
    main()
