# Main File to test the Graph Class
# L & S Gonnord, 2016
from LibGraphes_bibi import *

def main():
    g1 = {"a" : ["d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"],
          "f" : [] }
    
    g2 = { "r3" : ["r1", "r2"],
           "r2" : ["r3", "r1", "c", "a"],
           "r1" : ["r3", "r2", "c"],
           "c"  : ["r1", "r2", "b", "a", "d", "e"],
           "b"  : ["a", "c", "d", "e"],
           "e"  : ["b", "c", "d"],
           "a"  : ["b", "c", "d", "r2"],
           "d"  : ["a", "b", "c", "e"] }

    exo4_TD1 = {   "1" : ["4", "3", "2"],
                   "2" : ["1", "7"],
                   "3" : ["1", "4", "5", "6"],
                   "4" : ["1", "3", "8"],
                   "5" : ["3", "6"],
                   "6" : ["3", "5", "7"],
                   "7" : ["2", "6"],
                   "8" : ["4"] }
    
    exo4_TD1bis = {"1" : ["2", "7", "8"],
                   "2" : ["1", "3", "4"],
                   "3" : ["2", "8", "10"],
                   "4" : ["2", "8"],
                   "5" : ["6", "8", "9", "10", "11"],
                   "6" : ["5", "7", "8"],
                   "7" : ["1", "6", "9"],
                   "8" : ["1", "3", "4", "5", "6"],
                   "9" : ["5", "7", "11"],
                   "10": ["3", "5"],
                   "11": ["5", "9"]}

#two graphs
    graph1 = Graphe(g1)
    graph2 = Graphe(g2)
        
    print("Sommets du graphe 1 :") 
    print(graph1.listeSommets())
    print("Aretes du graphe 1 :")
    print(graph1.listeAretes())
    print("Voisins de a dans le graphe 1 : ")
    print(graph1.listeVoisins('a'))
    print("Ajouter un sommet z au graphe 1 :") 
    graph1.ajouterSommet("z")
    print("Sommets du graphe 1 :") 
    print(graph1.listeSommets())
    print("Ajouter l'arete a - z :")
    graph1.ajouterArete(("a","z"))
    print("Ajouter l'arete a - a :")
    graph1.ajouterArete(("a","a"))
    print("Ajouter l'arete x - y où x et y sont des nouveaux sommets :")
    graph1.ajouterArete(("x","y"))
    print("Sommets du graphe 1 :") 
    print(graph1.listeSommets())
    print("Aretes du graphe 1 :")
    print(graph1.listeAretes())
    print("Supprimer le sommet f du graphe 1 :") 
    graph1.supprimerSommet('f')
    print("supprimer l'arete x - y :")
    graph1.supprimerArete(("x","y"))
    print(graph1)
    print()
    print('parcours profondeur graph1 à partir de a puis d')
    print(graph1.parcoursDFS('a')) #['a', 'd', 'c', 'b', 'e', 'z']
    print(graph1.parcoursDFS('d')) #['d', 'a', 'z', 'c', 'b', 'e']
    print('parcours largeur graph1 à partir de ')
    print(graph1.parcoursBFS('d')) #['d', 'a', 'c', 'z', 'b', 'e']
    print('chemin entre a et e ?')
    print(graph1.cheminEntre('a','e'))
    print('chemin entre a et y ?')
    print(graph1.cheminEntre('a','y'))
    print('chemin entre a et a ?')
    print(graph1.cheminEntre('a','a'))
    print('composantes connexes du graphe1')
    print(graph1.composantesConnexes())
    print(graph1)
    print("peut on colorier avec 0 couleur ?")
    print(graph1.colorier(0))   #False
    print("peut on colorier avec 3 couleurs ?")
    print(graph1.colorier(3))   #{'a': 1, 'c': 1, 'b': 0, 'e': 0, 'd': 0, 'y': 0, 'x': 1, 'z': 0} si arete x-y   
    print()
    print("Sommets du graphe 2 :") 
    print(graph2.listeSommets())
    print("Aretes du graphe 2 :")
    print(graph2.listeAretes())
    print("Voisins de a dans le graphe 2 : ")
    print(graph2.listeVoisins('a'))
    print("colorier le graphe 2 avec 4 couleurs ?")
    print(graph2.colorier(4))

    print("colorier le graphe 2 avec 3 couleurs ?")
    print(graph2.colorier(3))

    #graph2.print_dot('graphe2',graph2.colorier(4))

    print()
    print()
    print('exo4-5 TD1')
    graph = Graphe(exo4_TD1)
    print(graph.parcoursBFS('1'))      #['1', '2', '3', '4', '7', '5', '6', '8']
    #print(graph.parcoursBFS_rec('1'))
    print(graph.parcoursDFS('1'))      #['1', '2', '7', '6', '3', '4', '8', '5']
    #print(graph.parcoursDFS_rec('1')) 
    print('le graphe contient il un cycle ?')
    print(graph.contientCycle())
    print()
    print('exo4-5 TD1')
    graphbis = Graphe(exo4_TD1bis)
    print(graphbis.parcoursBFS('1'))   #['1', '2', '7', '8', '3', '4', '6', '9', '5', '10', '11']
    #print(graphbis.parcoursBFS_rec('1'))
    print(graphbis.parcoursDFS('1'))   #['1', '2', '3', '8', '4', '5', '6', '7', '9', '11', '10']
    #print(graphbis.parcoursDFS_rec('1'))
    print('le graphe contient il un cycle ?')
    print(graphbis.contientCycle())
    
if __name__ == '__main__':
    main()
