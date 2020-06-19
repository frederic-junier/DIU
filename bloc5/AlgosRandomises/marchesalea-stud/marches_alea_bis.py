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
  DANS LE PLAN puis l'espace
"""


def pas2():  # 4 directions équiprobables
    return [[1, 0], [0, 1], [-1, 0], [0, -1]][randint(0, 4)]


def marche2(nb_pas):
    X, Y, mX, mY = 0, 0, [0], [0]
    # TODO
    return mX, mY



def dessine_une_marche2_aux(nb_pas):
    les_x, les_y = marche2(nb_pas)
    pypl.clf()
    pypl.plot(les_x, les_y)
    pypl.plot([0, les_x[-1]], [0, les_y[-1]], marker='o', color='red')
    pypl.grid()
    pypl.savefig('marche_plan_%i.pdf' % nb_pas)


def dessine_marche2():
    for nb_pas in [100, 10000]:
        dessine_une_marche2(nb_pas)

def distance_moyenne2(nb_pas, nb_marches):
    s = 0
    # TODO
    return s / nb_marches

def distance_carre_moyenne2(nb_pas, nb_marches):
    s = 0
    # TODO
    return s / nb_marches

def repasse_par2(objectif, nb_pas):
    x, y = 0, 0
    # TODO
    return False


def proba_passage2(objectif, nb_pas, nb_marches):
    cpt = 0
    # TODO
    return cpt/nb_marches


"""
  DANS L'ESPACE
"""

# TODO à vous !


"""
  SUR LE CERCLE TRIGONOMÉTRIQUE 
"""

# TODO à vous !



if __name__ == '__main__':
    print("dans le plan")
    # TODO
