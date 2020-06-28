#!/usr/bin/env python3

# Main File to test 


##############  Imports des modules #####################

from lib_graphes_junier_frederic import *
from functools import wraps
import subprocess
import os.path
import sys



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
def test_graph(title= "Test", graph_dict = None, relative_path = "images/directgraph", cycle = False, pdf=False, greedy = False, dfs = False):
    """Test d'un graphe orienté donné par son dictionnaire d'adjacence"""
    print('*' * 30 + f'DEBUT DU TEST {test_graph.compteur}' + '*' * 30)
    print(title)
    directgraph = DirectGraph(graph_dict=graph_dict)
    print("Affichage du graphe de contraintes dans la console ")
    print(directgraph)
    #génération du pdf avec graphviz si pdf == True
    if pdf:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(dir_path, relative_path + str(test_graph.compteur))
        print("Dessin du graphe en pdf avec GraphViz")
        directgraph.print_dot(output_path)
    #Détection de cycle
    has_cycle = directgraph.detect_cycle()
    #assertion de vérification du résultat
    assert has_cycle == cycle, "Erreur dans la détection de cycle"
    print("Détection de cycle dans le graphe orienté, réponse : ", has_cycle)   
    #Tri topologique glouton
    if greedy: 
        (rep, order) = directgraph.topological_sort_greedy()  
        #assertion de vérification du résultat
        assert (cycle == (not rep)) and  (directgraph.verif_topological_order(order) == True), f"Erreur dans le tri topologique glouton"
        print(f"Tri topologique de directgraph version gloutonne / notice de montage possible : {not has_cycle}, ordre pour la notice de montage : ", order)
    if dfs:
        (rep, order) = directgraph.topological_sort_dfs()
        #assertion de vérification du résultat
        assert (cycle == (not rep)) and (directgraph.verif_topological_order(order) == True), f"Erreur dans le tri topologique dfs" 
        print(f"Tri topologique de directgraph version dfs / notice de montage possible : {not has_cycle},  ordre pour la notice de montage : ", order)
    print('*' * 31 + f'FIN DU TEST {test_graph.compteur}' + '*' * 31)


def main(pdf =  False, greedy = True, dfs  = True):
    """Regroupe les exemples pour les test"""


    test_graph(title = "Un graphe orienté de contraintes avec cycle",
               graph_dict={"a" : ["h"], "b" : [], "c" : ["a", "b", "e"], "d": ["b","c"], "e" : ["h","f"],
                                             "f" : [], "g" : ["e"], "h" : [], "i" : ["e"]},
                cycle = False, pdf = pdf, greedy = greedy, dfs = dfs)
    
    test_graph(title = "Un graphe orienté de contraintes avec cycle", 
               graph_dict={"a" : ["c"], "b" : ["a"], "c" : ["d", "e"],
                            "d" : ["b"], "e" : [], "f" : ["c"] },                            
               cycle = True, pdf = pdf, greedy = greedy, dfs = dfs)

    test_graph(title = "Un graphe orienté de contraintes sans cycle", 
                graph_dict={"a" : ["b", "c"], "b" : ["d", "e"], "c" : ["g", "e"], "d": ["f"], "e" : ["f"],
                                             "f" : ["j", "k"], "g" : [], "h" : ["g"], "i" : ["h"], 
                                             "j" : ["k","i"], "k" : ["l"], "l":[]},
                cycle = False, pdf = pdf, greedy = greedy, dfs = dfs)

    test_graph(title = "Un graphe orienté de contraintes avec cycle",
               graph_dict={"a" : ["b", "c"], "b" : ["d", "e"], "c" : ["a", "e"], "d": ["f"], "e" : ["f"],
                                             "f" : ["j", "k"], "g" : ["c"], "h" : ["g"], "i" : ["h"], 
                                             "j" : ["k","i"], "k" : ["l"], "l":[]},
                cycle = True, pdf = pdf, greedy = greedy, dfs = dfs)

    

    test_graph(title = "Un graphe orienté de contraintes sans cycle", 
               graph_dict={"a" : ["b","c"], "b" : ["e","f"], "c" : [ "e"],
                             "d": [], "e" : [], "f" : ["e"]},
                cycle = False, pdf = pdf, greedy = greedy, dfs = dfs)



############################ Exécution du programme principal #############################
if __name__ == "__main__":

    arguments = list(map(lambda c : str.lstrip(c, '-'), map(str.lower, sys.argv)))
    #le premier arguments récupéré dans sys.argv est le nom du script qui ne nous intéresse pas
    #dictionnaire des arguments à passer à la fonction main
    kwargs = {arg : True for arg in arguments[1:]}
    print(kwargs)
    if  'h' in arguments or 'help' in arguments:
        print("""Utilisation du script MainJunierFrederic.py :
        * 'python MainJunierFrederic.py h' ou  'python MainJunierFrederic.py -h' ou 'python MainJunierFrederic.py --h' pour afficher l'aide
        * 'python MainJunierFrederic.py pdf' ou  'python MainJunierFrederic.py -pdf' ou  'python MainJunierFrederic.py --pdf' pour générer les pdf des graphes dans un sous-répertoire 'images'
        du répertoire courant    
        * 'python MainJunierFrederic.py greedy' pour tester la méthode de tri topologique gloutonne
        * 'python MainJunierFrederic.py dfs' pour tester la méthode de tri topologique avec dfs
        """)
    else:
        main(**kwargs)
        if 'pdf'in arguments  or 'png' in arguments:
            try:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                images_path = os.path.join(dir_path, 'images')
                #conversion de tous les graphes en png pour l'affichage dans le fichier README.md sous Gitlab ou Github
                subprocess.call(f"cd  {images_path} && ls *.pdf | sed s/pdf//g | xargs -I% convert %pdf %png", shell=True)
            except SystemError:
                print(f"""Erreur dans l'exécution de la commande `cd  {images_path} && ls *.pdf | sed s/pdf//g | xargs -I% convert %pdf %png`
                *  xargs pas installé ? sudo apt install findutils
                * convert pas installé ? sudo apt install imagemagick
                """)
   



   

