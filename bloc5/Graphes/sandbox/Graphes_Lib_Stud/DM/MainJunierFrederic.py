# Main File to test 


##############  Imports des modules #####################

from LibGraphesJunierFrederic import *
from functools import wraps
import subprocess


#############  Fonctions outils ###########################

def counter(f):
    """Décorateur pour compter les appels à une fonction"""

    @wraps(f)
    def wraped(*args, **kwargs):
        wraped.compteur += 1
        return f(*args, **kwargs)

    wraped.compteur = 0
    return wraped



#ici le compteur d'appel servira à numéroter les noms de fichiers de graphes
@counter
def test_graph(title= "Test", graph_dict = None, name = "directgraph", cycle = False):
    print('*' * 30 + f'DEBUT DU TEST {test_graph.compteur}' + '*' * 30)
    print(title)
    directgraph = DirectGraph(graph_dict=graph_dict)
    print("Affichage du graphe dans la console ")
    print(directgraph)
    print("Dessin du graphe en pdf avec GraphViz")
    directgraph.print_dot(name + str(test_graph.compteur))
    has_cycle = directgraph.detect_cycle()
    #assertion de vérification du résultat
    assert has_cycle == cycle, "Erreur dans la détection de cycle"
    print("Détection de cycle dans le graphe orienté, réponse : ", has_cycle)    
    (rep, order) = directgraph.topological_sort()  
    #assertion de vérification du résultat
    assert (cycle == (not rep)) and  (directgraph.verif_topological_order(order) == True), f"Erreur dans le tri topologique glouton"
    print("Tri topologique de directgraph version gloutonne : ", order)
    (rep, order) = directgraph.topological_sort_dfs()
    #assertion de vérification du résultat
    assert (cycle == (not rep)) and (directgraph.verif_topological_order(order) == True), f"Erreur dans le tri topologique dfs" 
    print("Tri topologique de directgraph version dfs", order)
    print('*' * 31 + f'FIN DU TEST {test_graph.compteur}' + '*' * 31)


def main():
    """Regroupe les exemples pour les test"""
    
    test_graph(title = "Un graphe orienté avec cycle", 
               graph_dict={"1" : ["2", "4"], "2" : [], "3" : ["2", "5"],
                            "4" : ["6"], "5" : ["4", "3"], "6" : [] },                            
               cycle = True)

    test_graph(title = "Un graphe orienté sans cycle", 
                graph_dict={"1" : ["2", "3"], "2" : ["4", "5"], "3" : ["7", "5"], "4": ["6"], "5" : ["6"],
                                             "6" : ["10", "11"], "7" : [], "8" : ["7"], "9" : ["8"], 
                                             "10" : ["11","9"], "11" : ["12"], "12":[]},
                cycle = False)

    test_graph(title = "Un graphe orienté avec cycle",
                graph_dict={"1" : ["2", "3"], "2" : ["4", "5"], "3" : ["5"], "4": ["6"], "5" : ["6"],
                                             "6" : ["10", "11"], "7" : ["3"], "8" : ["7"], 
                                             "9" : ["8"], "10" : ["11","9"], "11" : ["12"], "12":[]},
                cycle = True)

    test_graph(title = "Un graphe orienté avec cycle",
               graph_dict={"1" : ["8"], "2" : [], "3" : ["1", "2", "5"], "4": ["2","3"], "5" : ["8","6"],
                                             "6" : [], "7" : ["5"], "8" : [], "7" : ["5"], "8" : [], 
                                             "9" : ["5"]},
                cycle = False)

    test_graph(title = "Un graphe orienté sans cycle", 
               graph_dict={"1" : ["2","3"], "2" : ["4","5"], "3" : [ "5"],
                             "4": [], "5" : [], "6" : ["5"]},
                cycle = False)



############################ Exécution du programme principal #############################
if __name__ == "__main__":
    main()
    try:
        #conversion de tous les graphes en png pour l'affichage dans le fichier README.md sous Gitlab ou Github
        subprocess.call("ls *.pdf | sed s/pdf//g | xargs -I% convert %pdf %png", shell=True)
    except SystemError:
        print("Erreur, xargs pas installé ? sudo apt install findutils")

