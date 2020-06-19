# -*- coding: utf-8 -*-
"""
Marches aléatoires
TP conçu par Stéphane Gonnord pour PSI999, 2019/2020
Usage : python3 marches_alea.py
"""

__author__ = "Stéphane Gonnord, modifié à la marge par Laure Gonnord <Laure.Gonnord@univ-lyon1.fr>"
__version__ = "0.3 Mai 2020"


from numpy.random import random, randint
import matplotlib.pyplot as pypl
from numpy import sqrt, array, cos, sin, pi


"""
MARCHES DANS UNE RUE, avec ou sans biais
"""

def pas(p):  # p = proba d'aller à droite
    if random() < p:
        return 1
    else:
        return -1


def marche(nb_pas, p):
    X, m = 0, [0]
    # TODO : Une marche à p pas.
    return m

def dessine_une_marche_aux(nb_pas, p):
    les_t = range(nb_pas+1)
    les_y = marche(nb_pas, p)
    if not len(les_y) == nb_pas+1 :
        print("erreur : souci dans la fonction marche, j'arrete le dessin")
        exit(0)
    else:
        pypl.plot(les_t, les_y)

def dessine_marches():
    for nb_pas in [100, 1000, 10000]:
        pypl.clf()
        for _ in range(10):
            dessine_une_marche_aux(nb_pas, 0.5)
            pypl.grid()
            pypl.savefig('marche_%i.pdf' % nb_pas)
            pypl.clf()
        for _ in range(10):
            dessine_une_marche_aux(nb_pas, 0.7)
            pypl.grid()
            pypl.savefig('marche_biaisee_%i.pdf' % nb_pas)


def valeur_moyenne(nb_pas, p, nb_marches):
    res = 0
    # TODO 
    return res



def distance_moyenne(nb_pas, p, nb_marches):
    res = 0
    # TODO
    return res 
    


def distance_carre_moyenne(nb_pas, p, nb_marches):
    # TODO
    return 0



def repasse_par(objectif, nb_pas, p):  # toujours avec p = proba(droite)
    x = 0
    # TODO
    return False


def proba_passage(objectif, nb_pas, nb_marches, p):
    cpt = 0
    # TODO
    return cpt/nb_marches

if __name__ == '__main__':
    print(" 3 marches dans Z" )
    for i in range(3):
        print(marche(10, 0.5))
    print(" 1 marche biaisée dans Z" )
    print(marche(10, 0.3))
    print("dessin de marches regarder les fichiers générés")
    dessine_marches()
    # à vous, tester les probas, les valeurs moyennes, etc
    print("tests persos")
    # TODO
