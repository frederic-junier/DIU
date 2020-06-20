# Main File to test the Graph Class
# L & S Gonnord, 2016
from LibGraphes_bibi import *

def main():
    g1 = { "a" : ["d"],
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
    graph1 = Graphe(g1)
    graph2 = Graphe(g2)
        
#     print("Sommets du graphe 1 :") 
#     print(graph1.listeSommets())
#     print("Aretes du graphe 1 :")
#     print(graph1.listeAretes())
#     print("Voisins de a dans le graphe 1 : ")
#     print(graph1.listeVoisins('a'))
#     print("Ajouter un sommet z au graphe 1 :") 
#     graph1.ajouterSommet("z")
#     print("Sommets du graphe 1 :") 
#     print(graph1.listeSommets())
#     print("Ajouter l'arete a - z :")
#     graph1.ajouterArete(("a","z"))
#     print("Ajouter l'arete a - a :")
#     graph1.ajouterArete(("a","a"))
#     print("Ajouter l'arete x - y où x et y sont des nouveaux sommets :")
#     graph1.ajouterArete(("x","y"))
#     print("Sommets du graphe 1 :") 
#     print(graph1.listeSommets())
#     print("Aretes du graphe 1 :")
#     print(graph1.listeAretes())
#     print("Supprimer le sommet f du graphe 1 :") 
#     graph1.supprimerSommet('f')
#     print("supprimer l'arete x - y :")
#     graph1.supprimerArete(("x","y"))
#     print(graph1)
#     print()
#     print(graph1.parcoursDFS('a')) #['a', 'z', 'd', 'c', 'e', 'b']
#     print(graph1.parcoursDFS('d')) #['d', 'c', 'e', 'b', 'a', 'z']
#     print(graph1.parcoursBFS('d')) #['d', 'a', 'c', 'z', 'b', 'e']
#     print(graph1.cheminEntre('a','e'))
#     print(graph1.cheminEntre('a','y'))
#     print(graph1.composantesConnexes())
#     print(graph1)
#     print(graph1.color(0))   #False
#     print(graph1.color(3))   #{'a': 1, 'c': 1, 'b': 0, 'e': 0, 'd': 0, 'y': 0, 'x': 1, 'z': 0} si arete x-y   
#     print(graph1.colorier(3))
#     print()
    print("Sommets du graphe 2 :") 
    print(graph2.listeSommets())
    print("Aretes du graphe 2 :")
    print(graph2.listeAretes())
    print("Voisins de a dans le graphe 2 : ")
    print(graph2.listeVoisins('a'))
    print(" les graphe 2 avec 4 couleurs ?")
    print(graph2.color(4))
    print(graph2.colorier(4))
    print("colorier les graphe 2 avec 3 couleurs ?")
    print(graph2.color(3))
    print(graph2.colorier(3))
    graph2.print_dot('graphe2',graph2.colorier(4))


if __name__ == '__main__':
    main()
