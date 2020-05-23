# %%
from functools import wraps, reduce, lru_cache
import time

###############################################################################
# TP : pratique de la programmation fonctionnelle en Python
#
# Cette feuille de TP a pour but de vous familiariser avec la programmation fonctionnelle.
# Elle est composée des parties suivantes :
# 1. une introduction avec des versions itératives/récursives de Fibonacci et de la factorielle
# 2. une variation sur le thème de la fonction "forall" qui teste si tous les éléments d'une liste satisfont un prédicat
#   * vous utiliserez à cette occasion les briques de base de la programmation fonctionnelle, disponibles dans la bibliothèque standard de Python
# 3. un introduction aux décorateurs, des fonctions "qui modifient le comportement d'autres fonction"
# 4. la découverte des fonctionnalités spécifiques des décorateurs en Python qui doit vous amener à une application utile en classe avec les élèves
###############################################################################

# %%
###############################################################################
# INTRODUCTION : VERSION ITÉRATIVES ET RÉCURSIVES D'UN MÊME ALGORITHME
###############################################################################


def gen_examples(f, n=10):
    """Pour générer les (n + 1) premiers termes f(0), f(1), ..., f(n)"""
    return [f(i) for i in range(0, n)]



########################################
# EXERCICE : donner une version itérative de fibo_rec
########################################


# On donne la fonction fibo_rec (suite de Fibonacci) suivante


def fibo_rec(n):
    """Suite de Fibonacci, version récursive"""
    if n <= 1:
        return n
    else:
        return fibo_rec(n-1) + fibo_rec(n-2)


def fibo_iter(n):
    """TODO Suite de Fibonacci, version itérative"""
    pass


# print(f"fibo_rec  = {gen_examples(fibo_rec)}")
# print(f"fibo_iter = {gen_examples(fibo_iter)}")
# ATTENDU
# fibo_rec  = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
# fibo_iter = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


########################################
# EXERCICE :  donner une version recursive de fact_iter
########################################

# On donne la fonction factorielle suivante :


def fact_iter(n):
    """Factorielle, version itérative"""
    r = 1
    for i in range(1, n + 1):
        r *= i
    return r


def fact_rec(n):
    """TODO factorielle, version récursive"""
    pass


# print("Les premiers termes de la factorielle")
# print(f"fact_iter = {gen_examples(fact_iter)}")
# print(f"fact_rec  = {gen_examples(fact_rec)}")
# ATTENDU
# fact_iter = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
# fact_rec  = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

# %%
###############################################################################
# PROGRAMMATION FONCTIONNELLE AVEC DES VARIANTES DE FORALL
###############################################################################

# On va définir la fonction suivante forall, de plusieurs façons différentes
# La fonction forall prend en paramètres
#   * une fonction pred (apellée prédicat)
#   * une liste l
# forall retourne True ssi tous les x dans l sont tels que pred(x)==True

ex1 = [4, 4, 2, 0, 1]
ex2 = []
ex3 = [4, 4, 2, 0, 8]
def pair(x): return x % 2 == 0

########################################
# EXERCICE :  définir forall (version boucle for)
########################################


def forall_for(pred, l):
    """TODO : une version de forall avec une boucle for """
    pass


# print(f"forall_for(pair, ex1)={forall_for(pair, ex1)}")
# print(f"forall_for(pair, ex2)={forall_for(pair, ex2)}")
# print(f"forall_for(pair, ex3)={forall_for(pair, ex3)}")
# ATTENDU
# forall_for(pair, ex1)=False
# forall_for(pair, ex2)=True
# forall_for(pair, ex3)=True


########################################
# EXERCICE :  définir forall (version récursive avec les listes)
########################################


# Pour cet exercice, on se dote des fonctions suivantes


def empty(l):
    """Retourne True ssi la liste est vide"""
    return len(l) == 0


def head(l):
    """Retourne la tête de la liste, son 1er élément, et None si la liste est vide"""
    if empty(l):
        return None
    return l[0]


def tail(l):
    """Retourne la liste privée de son 1er élément, et None si la liste est vide"""
    if empty(l):
        return None
    return l[1:]


def forall_funct(pred, l):
    """TODO : une version récursive de forall, plus fonctionnelle, utilisant UNIQUEMENT empty, head et tail, sans boucle for ni affectation. La fonction sera récursive"""
    pass


# print(f"forall_funct(pair, ex1)={forall_funct(pair, ex1)}")
# print(f"forall_funct(pair, ex2)={forall_funct(pair, ex2)}")
# print(f"forall_funct(pair, ex3)={forall_funct(pair, ex3)}")
# ATTENDU
# forall_funct(pair, ex1)=False
# forall_funct(pair, ex2)=True
# forall_funct(pair, ex3)=True

########################################
# EXERCICE :  définir forall (version avec map)
########################################


def forall_map_all(pred, l):
    """TODO : une version de forall utilisant les fonctions map et all de la bibliothèque standard
    voir https://docs.python.org/3/library/functions.html"""
    pass


# print(f"forall_map_all(pair, ex1)={forall_map_all(pair, ex1)}")
# print(f"forall_map_all(pair, ex2)={forall_map_all(pair, ex2)}")
# print(f"forall_map_all(pair, ex3)={forall_map_all(pair, ex3)}")
# ATTENDU
# forall_map_all(pair, ex1)=False
# forall_map_all(pair, ex2)=True
# forall_map_all(pair, ex3)=True

########################################
# EXERCICE :  définir forall (version avec filter)
########################################


def forall_filter(pred, l):
    """TODO : une version de forall utilisant les fonctions standards filter et len. On pourra avoir besoin de transformer le résultat intermédiaire avec list()"""
    pass


# print(f"forall_filter(pair, ex1)={forall_filter(pair, ex1)}")
# print(f"forall_filter(pair, ex2)={forall_filter(pair, ex2)}")
# print(f"forall_filter(pair, ex3)={forall_filter(pair, ex3)}")
# ATTENDU
# forall_filter(pair, ex1)=False
# forall_filter(pair, ex2)=True
# forall_filter(pair, ex3)=True

########################################
# EXERCICE :  définir forall (version avec reduce)
########################################

# La fonction standard reduce du module functools (appelée aussi fold) prend trois paramètre
#    * une fonction f  de type A * B -> A
#    * une liste l de type [A]
#    * une valeur initiale x0 de type A
# Pour l = [x1, x2, ..., xn], reduce(f, l, x0) calcule
# f(...(f(f(x0, x1), x2)...), xn)
# Par exemple, reduce(lambda acc, x : acc * x, range(1,6), 1) calcule
# ((((((1*1)*2)*3)*4)*5)*6) = 6! = 120
# print( f"reduce(lambda acc, x : acc * x, range(1,6), 1)={reduce(lambda acc, x : acc * x, range(1,6), 1)}")

# https://docs.python.org/3/library/functools.html#functools.reduce


def forall_reduce(pred, l):
    """TODO : une version de forall utilisant UNIQUEMENT la fonction standard functools.reduce
    """
    pass


# print(f"forall_reduce(pair, ex1)={forall_reduce(pair, ex1)}")
# print(f"forall_reduce(pair, ex2)={forall_reduce(pair, ex2)}")
# print(f"forall_reduce(pair, ex3)={forall_reduce(pair, ex3)}")
# ATTENDU
# forall_reduce(pair, ex1)=False
# forall_reduce(pair, ex2)=True
# forall_reduce(pair, ex3)=True

# %%
###############################################################################
# LES DÉCORATEURS EN PYTHON
###############################################################################

# Un décorateur est une fonction qui modifie le comportement d'une autre fonction.
# Plus précisément, c'est une fonction d qui prend une fonction f (unaire) en argument,
# telle que d(f) est la fonction f dont le comportement est modifié.
# La fonction d est donc une fonction d'ordre supérieur qui prend une fonction en argument et en renvoie une.

# Un exemple, le décorateur qui affiche le temps d'exécution. On ne gère ici que le cas où f est unaire


def timer(f):
    """Calcule et affiche la durée d'exécution d'une fonction unaire"""
    def wrapped(x):
        start = time.time()
        value = f(x)
        end = time.time()
        print(f"Durée {end - start}  secs")
        return value
    return wrapped


# On peut se servir pour chronométrer une des fonctions précédentes, par exemple fibo_rec(32) qui prend un temps sensible (~1 sec. sur ma machine)
# print(timer(fibo_rec)(32))
# ATTENDU
# Durée 0.8552179336547852  secs
# 2178309

# %%
########################################
# EXERCICE : définir le décorateur maybe
########################################


def maybe(f, v):
    """Appelle f et si f renvoie None, alors renvoie v à la place. Autrement dit, maybe(f, v) fait la même chose que f sauf pour les entrées où f est indéfinie"""
    pass


def positive_or_none(n):
    if n < 0:
        return None
    return n


# positive_or_zero = maybe(positive_or_none, 0)

# print(f"positive_or_none(42)={positive_or_none(42)}")
# print(f"positive_or_none(-1)={positive_or_none(-1)}")
# print(f"positive_or_zero(42)={positive_or_zero(42)}")
# print(f"positive_or_zero(-1)={positive_or_zero(-1)}")
# ATTENDU
# positive_or_none(42)=42
# positive_or_none(-1)=None
# positive_or_zero(42)=42
# positive_or_zero(-1)=0



########################################
# EXERCICE : définir le décorateur maybe avec des lambda fonctions uniquement
########################################

# Même question que précédemment, mais écrire maybe UNIQUEMENT avec des lambdas et
# une expression conditionnelle (dit aussi if ternaire)
# https://docs.python.org/3/reference/expressions.html#conditional-expressions

maybe_lambda = lambda f,v : None


# positive_or_zero_lambda = maybe_lambda(positive_or_none, 0)

# print(f"positive_or_zero_lambda(42)={positive_or_zero_lambda(42)}")
# print(f"positive_or_zero_lambda(-1)={positive_or_zero_lambda(-1)}")
# ATTENDU
# positive_or_zero_lambda(42)=42
# positive_or_zero_lambda(-1)=0

########################################
# EXERCICE (POUR ALLER PLUS LOIN)
########################################

# même chose que précédemment, maybe uniquement avec des lambdas mais en faisant attention à n'appeler f QU'UNE SEULE FOIS

maybe_lambda_better = lambda f,v : None


# positive_or_zero_lambda_better = maybe_lambda(positive_or_none, 0)

# print(
#     f"positive_or_zero_lambda_better(42)={positive_or_zero_lambda_better(42)}")
# print(
#     f"positive_or_zero_lambda_better(-1)={positive_or_zero_lambda_better(-1)}")
# ATTENDU
# positive_or_zero_lambda_better(42)=42
# positive_or_zero_lambda_better(-1)=0

########################################
# EXERCICE (POUR ALLER PLUS LOIN) : maybe n-aire
########################################

# même question qu'au début, mais dans le cas général où f est une fonction n-aire
# utiliser pour cela https://book.pythontips.com/en/latest/args_and_kwargs.html


def maybe_nary(f, v):
    """Appelle f et si f renvoie None, alors renvoie v à la place. Autrement dit, maybe(f, v) fait la même chose que f sauf pour les cas où f est indéfinie"""
    pass


def any_positive_or_none(*args):
    """Return None if any argument is negative and the list of its argument otherwise"""
    for arg in args:
        if arg < 0:
            return None
    return list(args)


# any_positive_or_zero = maybe_nary(any_positive_or_none, [])


# print(f"any_positive_or_zero(42)={any_positive_or_zero(42)}")
# print(f"any_positive_or_zero(-1)={any_positive_or_zero(-1)}")
# print(f"any_positive_or_zero(1,2,3,-1)={any_positive_or_zero(1,2,3,-1)}")
# print(f"any_positive_or_zero(1,2,3)={any_positive_or_zero(1,2,3)}")
# ATTENDU
# any_positive_or_zero(42) = [42]
# any_positive_or_zero(-1) = []
# any_positive_or_zero(1, 2, 3, -1) = []
# any_positive_or_zero(1, 2, 3) = [1, 2, 3]

# %%
########################################
# EXERCICE : définir le décorateur memoize
########################################


def memoize(f):
    """memoize permet de mémoriser les appels de f : si memoize(f) a déjà été appelée avec le même argument, alors memoize(f) renvoie directement (sans rappeler relancer le calcul de f) la valeur retournée précédemment par f pour cet argument. On supposera f unaire et on utilisera un dictionnaire pour mémoriser les valeurs calculées"""
    pass


# def fonction_de_test(n):
#     print(f"    fonction_de_test appellée avec {n}")
#     return n*n


# fonction_de_test_memo = memoize(fonction_de_test)
# print(f"fonction_de_test_memo(42)={fonction_de_test_memo(42)}")
# print(f"fonction_de_test_memo(0)={fonction_de_test_memo(0)}")
# print(f"fonction_de_test_memo(42)={fonction_de_test_memo(42)}")
# print(f"fonction_de_test_memo(0)={fonction_de_test_memo(0)}")
# ATTENDU : On ne doit voir que 2 fois le print dans la fonction de test (et pas 4 sans memoize)
#     fonction_de_test appellée avec 42
# fonction_de_test_memo(42)=1764
#     fonction_de_test appellée avec 0
# fonction_de_test_memo(0)=0
# fonction_de_test_memo(42)=1764
# fonction_de_test_memo(0)=0

########################################
# EXERCICE  (POUR ALLER PLUS LOIN) : définir le décorateur memoize qui gère le cas des fonction n-aires (sans arguments de type keywords, autrement dit, on gère juste *args, pas **kwargs)
########################################


def memoize_nary(f):
    """Pour cette version, on devra convertir une "liste" de plusieurs paramètres (*args) en 
       une structure qui soit hashable pour pouvoir servir de clef dans le dictionnaire
       Les listes ne le sont pas, mais les tuples le sont en revanche."""
    pass


# def fonction_de_test_nary(*args):
#     print(f"    fonction_de_test appellée avec {list(args)}")
#     return [x*x for x in args]


# fonction_de_test_nary_memo = memoize_nary(fonction_de_test_nary)

# print(f"fonction_de_test_nary_memo(1,2,3)={fonction_de_test_nary_memo(1,2,3)}")
# print(f"fonction_de_test_nary_memo(0,1,2)={fonction_de_test_nary_memo(0,1,2)}")
# print(f"fonction_de_test_nary_memo(1,2,3)={fonction_de_test_nary_memo(1,2,3)}")
# print(f"fonction_de_test_nary_memo(0,1,2)={fonction_de_test_nary_memo(0,1,2)}")
# ATTENDU : on ne doit voir que 2 fois le print dans la fonction de test (et pas 4 sans memoize
#     fonction_de_test appellée avec [1, 2, 3]
# fonction_de_test_nary_memo(1,2,3)=[1, 4, 9]
#     fonction_de_test appellée avec [0, 1, 2]
# fonction_de_test_nary_memo(0,1,2)=[0, 1, 4]
# fonction_de_test_nary_memo(1,2,3)=[1, 4, 9]
# fonction_de_test_nary_memo(0,1,2)=[0, 1, 4]

# %%
###############################################################################
# LES DÉCORATEURS PYTHON DANS LA BIBLIOTHÈQUE STANDARD : UNE APPLICATION POUR LA CLASSE
###############################################################################

# /!\ Cet exercice vous amène à écrire un décorateur qui peut être très utile en classe pour illustrer la récursivité.
# Cet exercice est issu de discussions avec des étudiants en CAPES NSI qui souhaitaient,
# dans le cadre de la préparation du projet à présenter pour l'oral 2 du concours,
# fournir une petite bibliothèque pour aider les élèves à aborder cette notion.
# Je pense que le décorateur suivant pourrait en faire partie. /!\

# Python propose une syntaxe ad hoc @decorator pour la manipulation des décorateurs.
# De plus, la bibliothèque standard propose quelques outils pour en faciliter la manipulation ainsi que quelques décorateurs très utiles.
# Voir :
#
# https://docs.python.org/3/glossary.html#term-decorator
# https://docs.python.org/3/reference/compound_stmts.html#function
# https://book.pythontips.com/en/latest/decorators.html
# https://docs.python.org/3/library/functools.html


# Par exemple, avec le décorateur suivant @tracer, on peut tracer les appels à la fonction récursive qui calcule le n-ieme terme de la suite de Fibonacci


def tracer(func):
    """Un décorateur qui trace les exécutions"""
    # pour ne pas changer __name__ en 'wrapped' après wrapping, voir functools
    @wraps(func)
    def wrapped(*args, **kwargs):
        print(f'Calling {func.__name__}({args}, {kwargs})')
        return func(*args, **kwargs)
    return wrapped


@tracer
def fibo_tracee(n):
    """Suite de Fibonacci, version récursive avec les appels tracés"""
    if n <= 1:
        return n
    else:
        return fibo_tracee(n-1) + fibo_tracee(n-2)


# print(f"fibo_tracee(5)={fibo_tracee(5)}")
# ATTENDU
# Calling fibo_tracee((5,), {})
# Calling fibo_tracee((4,), {})
# Calling fibo_tracee((3,), {})
# Calling fibo_tracee((2,), {})
# Calling fibo_tracee((1,), {})
# Calling fibo_tracee((0,), {})
# Calling fibo_tracee((1,), {})
# Calling fibo_tracee((2,), {})
# Calling fibo_tracee((1,), {})
# Calling fibo_tracee((0,), {})
# Calling fibo_tracee((3,), {})
# Calling fibo_tracee((2,), {})
# Calling fibo_tracee((1,), {})
# Calling fibo_tracee((0,), {})
# Calling fibo_tracee((1,), {})
# fibo_tracee(5)=5


# /!\ IMPORTANT /!\ 
# On remarque immédiatement 2 choses :
# * cette implémentation est sous optimale car elle produit un nombre exponentiel d'appel récursifs
# * la profondeur des appels récursifs n'est pas visible, elle devrait l'être avec une indentation

########################################
# EXERCICE : écrire le décorateur @visualise
########################################


def visualise(func):
    """Décorateur qui trace les appels comme @tracer mais en indentant à chaque appel récursif"""
    visualise.level = 0
    pass


@visualise
def fibo_indent(n):
    """Suite de Fibonacci, version récursive avec les appels tracés ET indentés"""
    if n <= 1:
        return n
    else:
        return fibo_indent(n-1) + fibo_indent(n-2)


# print(f"fibo_indent(5)={fibo_indent(5)}")
# ATTENDU
# on doit obtenir quelque chose de semblable à la trace suivante
# fibo_indent((5,), {})
#     fibo_indent((4,), {})
#         fibo_indent((3,), {})
#             fibo_indent((2,), {})
#                 fibo_indent((1,), {})
#                 fibo_indent((0,), {})
#             fibo_indent((1,), {})
#         fibo_indent((2,), {})
#             fibo_indent((1,), {})
#             fibo_indent((0,), {})
#     fibo_indent((3,), {})
#         fibo_indent((2,), {})
#             fibo_indent((1,), {})
#             fibo_indent((0,), {})
#         fibo_indent((1,), {})
# fibo_indent(5)=5


# On peut utiliser maintenant le décorateur de la bibliothèque standard @lru_cache ou votre décorateur @memoize pour optimiser le calcul des termes de la suite de Fibonacci !

@memoize
@visualise
def fibo_viz_memo(n):
    """Suite de Fibonacci, version récursive avec les appels tracés, indentés et mémorisés"""
    if n <= 1:
        return n
    else:
        return fibo_viz_memo(n-1) + fibo_viz_memo(n-2)


# print(f"fibo_viz_memo(5)={fibo_viz_memo(5)}")
# ATTENDU
# on doit obtenir quelque chose de semblable à la trace suivante
# fibo_viz_memo((5,), {})
#     fibo_viz_memo((4,), {})
#         fibo_viz_memo((3,), {})
#             fibo_viz_memo((2,), {})
#                 fibo_viz_memo((1,), {})
#                 fibo_viz_memo((0,), {})
# fibo_viz_memo(5)=5


# %%
